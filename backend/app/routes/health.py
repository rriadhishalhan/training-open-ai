"""
Health check endpoint for monitoring the service status.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status information indicating the service is healthy
    """
    return {"status": "ok"}
