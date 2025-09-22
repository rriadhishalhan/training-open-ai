from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional
import os
from datetime import datetime
from pathlib import Path

router = APIRouter()

UPLOADS_DIR = Path("processed_uploads")
ORIGINAL_UPLOADS_DIR = Path("uploads")

@router.get("/images")
async def list_images(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)
):
    """
    Get a paginated list of all processed images
    """
    try:
        # Ensure uploads directory exists
        if not UPLOADS_DIR.exists():
            return {"items": [], "total": 0, "page": page, "page_size": page_size}
        
        # List all files in processed_uploads directory
        all_files = []
        for file_path in UPLOADS_DIR.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                stats = file_path.stat()
                all_files.append({
                    "id": str(file_path.stem),  # Using filename without extension as ID
                    "filename": file_path.name,
                    "uploadDate": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    "url": f"/api/processed_uploads/{file_path.name}"
                })
        
        # Sort files by upload date (newest first)
        all_files.sort(key=lambda x: x["uploadDate"], reverse=True)
        
        # Calculate pagination
        total_items = len(all_files)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get paginated items
        items = all_files[start_idx:end_idx]
        
        return {
            "items": items,
            "total": total_items,
            "page": page,
            "page_size": page_size
        }
        
    except Exception as e:
        return {"error": str(e)}


@router.delete("/images/{image_id}")
async def delete_image(image_id: str):
    """
    Delete an image by ID. This will remove both the original and processed versions.
    
    Args:
        image_id: The ID of the image to delete (filename without extension)
        
    Returns:
        dict: Success message or error details
        
    Raises:
        HTTPException: If image not found or deletion fails
    """
    try:
        # Find and delete processed image
        processed_deleted = False
        original_deleted = False
        
        # Look for processed image
        for file_path in UPLOADS_DIR.glob("*"):
            if file_path.is_file() and (file_path.stem == image_id or image_id in file_path.name):
                try:
                    file_path.unlink()
                    processed_deleted = True
                    break
                except OSError as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to delete processed image: {str(e)}"
                    )
        
        # Look for original image in uploads directory
        for file_path in ORIGINAL_UPLOADS_DIR.glob("*"):
            if file_path.is_file() and image_id in file_path.name:
                try:
                    file_path.unlink()
                    original_deleted = True
                    break
                except OSError as e:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to delete original image: {str(e)}"
                    )
        
        # Check if any files were deleted
        if not processed_deleted and not original_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Image with ID '{image_id}' not found"
            )
        
        return {
            "message": f"Image '{image_id}' deleted successfully",
            "processed_deleted": processed_deleted,
            "original_deleted": original_deleted
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete image: {str(e)}"
        )