"""
Utility functions for image processing and drawing bounding boxes.
"""

import io
from typing import List

from PIL import Image, ImageDraw, ImageFont

from app.routes.detection import BoundingBox


def draw_bounding_boxes(image_data: bytes, boxes: List[BoundingBox]) -> bytes:
    """
    Draw bounding boxes on an image and return the modified image.

    Args:
        image_data: Original image as bytes
        boxes: List of bounding boxes to draw

    Returns:
        bytes: Modified image with bounding boxes drawn on it
    """
    # Open the image from bytes
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB if necessary (for JPEG output)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Define colors for different objects (will cycle through these)
    colors = [
        '#FF0000',  # Red
        '#00FF00',  # Green
        '#0000FF',  # Blue
        '#FFFF00',  # Yellow
        '#FF00FF',  # Magenta
        '#00FFFF',  # Cyan
        '#FFA500',  # Orange
    ]
    
    # Try to load a font
    try:
        # Try to use Arial for Windows
        font = ImageFont.truetype("arial.ttf", 20)
    except (OSError, IOError):
        try:
            # Try default font
            font = ImageFont.load_default()
        except Exception:
            font = None
    
    # Draw each bounding box
    for i, box in enumerate(boxes):
        # Get coordinates
        x1 = int(box.x)
        y1 = int(box.y)
        x2 = int(box.x + box.w)
        y2 = int(box.y + box.h)
        
        # Choose color for this box
        color = colors[i % len(colors)]
        
        # Draw rectangle
        draw.rectangle(
            [(x1, y1), (x2, y2)],
            outline=color,
            width=3
        )
        
        # Prepare label text
        label = f"{box.label} ({box.score:.2f})"
        
        # Calculate text background
        if font:
            bbox = draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Estimate text size if no font available
            text_width = len(label) * 8
            text_height = 15
            
        # Draw label background
        label_x = x1
        label_y = y1 - text_height - 4 if y1 > text_height + 4 else y2 + 4
        
        draw.rectangle(
            [(label_x, label_y), 
             (label_x + text_width + 4, label_y + text_height + 4)],
            fill=color
        )
        
        # Draw text
        draw.text(
            (label_x + 2, label_y + 2),
            label,
            fill='white',
            font=font
        )
    
    # Convert back to bytes
    output = io.BytesIO()
    image.save(output, format='JPEG', quality=95)
    output.seek(0)
    
    return output.getvalue()