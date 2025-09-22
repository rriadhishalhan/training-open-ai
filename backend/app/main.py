"""
FastAPI application main module.
"""

from pathlib import Path

from dotenv import load_dotenv
from app.routes import detection, health, upload
from fastapi import FastAPI

# Load environment variables from .env file at startup
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Bootcamp FastAPI Backend",
    description="A FastAPI service with health check, file upload, "
                "and object detection endpoints",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://localhost:5173",
                   "http://localhost:5174"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(detection.router, prefix="/api", tags=["detection"])

# Import and include images router
from app.routes import images
app.include_router(images.router, prefix="/api", tags=["images"])

# Mount uploads directory for serving uploaded files
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Mount directories for serving files
app.mount("/api/uploads", StaticFiles(directory=str(UPLOAD_DIR)),
          name="uploads")
app.mount("/api/processed_uploads", StaticFiles(directory=str(PROCESSED_DIR)),
          name="processed_uploads")


@app.get("/")
async def root():
    """Root endpoint returning basic information about the API."""
    return {
        "message": "Welcome to Bootcamp FastAPI Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
