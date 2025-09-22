"""
File upload endpoint for handling multipart form data.
"""

import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()

# Define upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(..., alias="files[]")):
    """
    Upload endpoint that accepts multiple files via multipart/form-data.

    Args:
        files: List of uploaded files (sent as 'files[]' from frontend)

    Returns:
        dict: Information about uploaded files including filenames, sizes, and
              saved paths

    Raises:
        HTTPException: If no files are provided or other upload errors occur
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    uploaded_files = []

    for file in files:
        if not file.filename:
            continue

        # Generate unique filename to prevent conflicts
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        try:
            # Read file content
            content = await file.read()
            file_size = len(content)

            # Save file to disk
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            uploaded_files.append({
                "original_filename": file.filename,
                "saved_filename": unique_filename,
                "file_path": str(file_path),
                "size": file_size,
                "content_type": file.content_type
            })

        except Exception as e:
            # Clean up partial file if it exists
            if file_path.exists():
                os.unlink(file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save file {file.filename}: {str(e)}"
            )

    if not uploaded_files:
        raise HTTPException(status_code=400, detail="No valid files uploaded")

    return {
        "message": "Files uploaded successfully",
        "files_count": len(uploaded_files),
        "files": uploaded_files,
        "upload_directory": str(UPLOAD_DIR.absolute())
    }
