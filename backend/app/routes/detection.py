"""
Azure Computer Vision Object Detection endpoint.
"""

import io
import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the .env file
env_path = Path(__file__).parents[3] / '.env'
logger.info(f"Looking for .env file at: {env_path}")

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Log environment variables (redacting sensitive info)
vision_endpoint = os.getenv("VISION_ENDPOINT")
vision_key = os.getenv("VISION_KEY")
logger.info(f"VISION_ENDPOINT loaded: {'Yes' if vision_endpoint else 'No'}")
logger.info(f"VISION_KEY loaded: {'Yes' if vision_key else 'No'}")

router = APIRouter()

# Upload and processed images directories
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed_uploads")
PROCESSED_DIR.mkdir(exist_ok=True)


class BoundingBox(BaseModel):
    """Normalized bounding box with label and confidence score."""
    label: str
    x: float
    y: float
    w: float
    h: float
    score: float


class DetectionResponse(BaseModel):
    """Response model for object detection results."""
    processed_image_url: str


async def call_azure_computer_vision(image_data: bytes) -> Dict[str, Any]:
    """
    Call Azure Computer Vision v3.2 Object Detection API.

    Args:
        image_data: Raw image bytes

    Returns:
        dict: Azure Computer Vision API response

    Raises:
        HTTPException: If API call fails
    """
    vision_endpoint = os.getenv("VISION_ENDPOINT")
    vision_key = os.getenv("VISION_KEY")

    if not vision_endpoint or not vision_key:
        logger.error("Azure Computer Vision credentials not configured")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Azure Computer Vision service not configured. "
                   "Please set VISION_ENDPOINT and VISION_KEY env vars."
        )

    # Construct the API URL
    analyze_url = f"{vision_endpoint.rstrip('/')}/vision/v3.2/analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": vision_key,
        "Content-Type": "application/octet-stream"
    }

    params = {
        "visualFeatures": "Objects"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                analyze_url,
                headers=headers,
                params=params,
                content=image_data
            )

            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Azure Computer Vision API error: " \
                    f"{response.status_code}"
                logger.error(f"{error_msg} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=error_msg
                )

    except httpx.TimeoutException:
        logger.error("Azure Computer Vision API timeout")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Azure Computer Vision API timeout"
        )
    except httpx.RequestError as e:
        logger.error(f"Azure Computer Vision API request error: {str(e)}")
        logger.error(f"Attempting to connect to: {analyze_url}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to connect to Azure Computer Vision API: {str(e)}"
        )


def normalize_detection_response(azure_response: Dict[str, Any]) -> \
        List[BoundingBox]:
    """
    Normalize Azure Computer Vision response to our standard format.

    Args:
        azure_response: Raw Azure Computer Vision API response

    Returns:
        List[BoundingBox]: Normalized bounding boxes
    """
    boxes = []

    if "objects" not in azure_response:
        logger.warning("No 'objects' field in Azure Computer Vision response")
        return boxes

    for obj in azure_response["objects"]:
        try:
            # Extract bounding box coordinates
            rect = obj.get("rectangle", {})
            x = rect.get("x", 0)
            y = rect.get("y", 0)
            width = rect.get("w", 0)
            height = rect.get("h", 0)

            # Extract label and confidence
            label = obj.get("object", "unknown")
            confidence = obj.get("confidence", 0.0)

            box = BoundingBox(
                label=label,
                x=float(x),
                y=float(y),
                w=float(width),
                h=float(height),
                score=float(confidence)
            )
            boxes.append(box)

        except (KeyError, ValueError, TypeError) as e:
            logger.warning(f"Failed to parse object detection result: {e}")
            continue

    return boxes


@router.get("/detections/{image_id}", response_model=DetectionResponse)
async def detect_objects(image_id: str):
    """
    Analyze an uploaded image for object detection using Azure Computer Vision.

    Args:
        image_id: The filename/ID of the uploaded image

    Returns:
        DetectionResponse: Normalized object detection results and URL to processed image

    Raises:
        HTTPException: If image not found or detection fails
    """
    try:
        # Find the image file in the upload directory
        image_path = None
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file() and image_id in file_path.name:
                image_path = file_path
                break

        if not image_path or not image_path.exists():
            logger.error(f"Image not found: {image_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with ID '{image_id}' not found"
            )

        # Read the image file
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
        except IOError as e:
            logger.error(f"Failed to read image file {image_path}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image file"
            )

        # Call Azure Computer Vision API
        azure_response = await call_azure_computer_vision(image_data)

        # Normalize the response
        boxes = normalize_detection_response(azure_response)

        # Process the image and save it
        processed_image_data = draw_bounding_boxes_on_image(image_data, boxes)
        processed_image_path = PROCESSED_DIR / f"processed_{image_id}"
        
        try:
            with open(processed_image_path, "wb") as f:
                f.write(processed_image_data)
        except IOError as e:
            logger.error(f"Failed to save processed image: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save processed image"
            )

        logger.info(f"Successfully detected {len(boxes)} objects in "
                    f"image {image_id} and saved processed image")
        
        # Return only the URL to the processed image
        return DetectionResponse(
            processed_image_url=f"/api/processed_uploads/processed_{image_id}"
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in object detection: {e}")
        # On any other failure, return empty boxes with error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Object detection failed due to an unexpected error"
        )


def draw_bounding_boxes_on_image(image_data: bytes, boxes: List[BoundingBox]) -> bytes:
    """
    Draw bounding boxes on an image and return the modified image as bytes.

    Args:
        image_data: Original image as bytes
        boxes: List of bounding boxes to draw

    Returns:
        bytes: Modified image with bounding boxes drawn
    """
    # Open the image
    image = Image.open(io.BytesIO(image_data))

    # Convert to RGB if necessary (for JPEG output)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Get image dimensions
    img_width, img_height = image.size

    # Define colors for different object types
    colors = [
        '#FF0000',  # Red
        '#00FF00',  # Green
        '#0000FF',  # Blue
        '#FFFF00',  # Yellow
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#FFA500',  # Orange
        '#800080',  # Purple
        '#FFC0CB',  # Pink
        '#A52A2A',  # Brown
    ]

    # Try to load a font, fall back to default if not available
    try:
        # Try to use a larger font for better visibility
        font = ImageFont.truetype("arial.ttf", 16)
    except (OSError, IOError):
        try:
            # Try default font
            font = ImageFont.load_default()
        except:
            font = None

    # Draw each bounding box
    for i, box in enumerate(boxes):
        # Convert normalized coordinates to pixel coordinates
        # Note: Azure CV returns absolute pixel coordinates, not normalized
        x1 = int(box.x)
        y1 = int(box.y)
        x2 = int(box.x + box.w)
        y2 = int(box.y + box.h)

        # Choose color based on object index
        color = colors[i % len(colors)]

        # Draw the bounding box rectangle
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        # Prepare label text
        label_text = f"{box.label} ({box.score:.2f})"

        # Calculate text size and position
        if font:
            bbox = draw.textbbox((0, 0), label_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Estimate text size if no font available
            text_width = len(label_text) * 8
            text_height = 12

        # Position label above the box, or below if there's no space above
        label_x = x1
        label_y = y1 - text_height - 5 if y1 - text_height - 5 > 0 else y2 + 5

        # Draw background rectangle for text
        draw.rectangle(
            [label_x, label_y, label_x + text_width + 4, label_y + text_height + 4],
            fill=color,
            outline=color
        )

        # Draw the text
        draw.text(
            (label_x + 2, label_y + 2),
            label_text,
            fill='white',
            font=font
        )

    # Save the modified image to bytes
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG', quality=95)
    output_buffer.seek(0)

    return output_buffer.getvalue()


@router.get("/detections/{image_id}/image")
async def get_image_with_detections(image_id: str):
    """
    Analyze an uploaded image for object detection and return the image with bounding boxes drawn.

    Args:
        image_id: The filename/ID of the uploaded image

    Returns:
        StreamingResponse: Image with bounding boxes drawn on it

    Raises:
        HTTPException: If image not found or detection fails
    """
    try:
        # Find the image file in the upload directory
        image_path = None
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file() and image_id in file_path.name:
                image_path = file_path
                break

        if not image_path or not image_path.exists():
            logger.error(f"Image not found: {image_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with ID '{image_id}' not found"
            )

        # Read the image file
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
        except IOError as e:
            logger.error(f"Failed to read image file {image_path}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to read image file"
            )

        # Call Azure Computer Vision API
        azure_response = await call_azure_computer_vision(image_data)

        # Normalize the response
        boxes = normalize_detection_response(azure_response)

        # Draw bounding boxes on the image
        processed_image_data = draw_bounding_boxes_on_image(image_data, boxes)

        logger.info(f"Successfully processed image {image_id} with {len(boxes)} objects")

        # Return the processed image
        return StreamingResponse(
            io.BytesIO(processed_image_data),
            media_type="image/jpeg",
            headers={"Content-Disposition": f"inline; filename=processed_{image_id}"}
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in image processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image processing failed due to an unexpected error"
        )
