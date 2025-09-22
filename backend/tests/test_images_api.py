import pytest
import tempfile
import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)

class TestImagesAPI:
    """Test suite for images API endpoints"""
    
    def setup_method(self):
        """Set up test fixtures before each test"""
        # Create temporary directories for testing
        self.test_uploads_dir = Path("test_processed_uploads")
        self.test_original_uploads_dir = Path("test_uploads")
        self.test_uploads_dir.mkdir(exist_ok=True)
        self.test_original_uploads_dir.mkdir(exist_ok=True)
        
        # Patch the directories in the images module
        import app.routes.images as images_module
        self.original_uploads_dir = images_module.UPLOADS_DIR
        self.original_original_uploads_dir = images_module.ORIGINAL_UPLOADS_DIR
        images_module.UPLOADS_DIR = self.test_uploads_dir
        images_module.ORIGINAL_UPLOADS_DIR = self.test_original_uploads_dir
    
    def teardown_method(self):
        """Clean up after each test"""
        # Restore original directories
        import app.routes.images as images_module
        images_module.UPLOADS_DIR = self.original_uploads_dir
        images_module.ORIGINAL_UPLOADS_DIR = self.original_original_uploads_dir
        
        # Clean up test files
        import shutil
        if self.test_uploads_dir.exists():
            shutil.rmtree(self.test_uploads_dir)
        if self.test_original_uploads_dir.exists():
            shutil.rmtree(self.test_original_uploads_dir)
    
    def create_test_image(self, filename="test_image.jpg", directory=None):
        """Create a test image file"""
        if directory is None:
            directory = self.test_uploads_dir
        
        test_file = directory / filename
        with open(test_file, "wb") as f:
            # Create a minimal fake image file
            f.write(b"fake image content")
        return test_file
    
    def test_list_images_empty(self):
        """Test listing images when no images exist"""
        response = client.get("/api/images")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert data["items"] == []
        assert data["total"] == 0
    
    def test_list_images_with_images(self):
        """Test listing images when images exist"""
        # Create test images
        self.create_test_image("test1.jpg")
        self.create_test_image("test2.png")
        self.create_test_image("test3.jpeg")
        self.create_test_image("not_image.txt")  # Should be ignored
        
        response = client.get("/api/images")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 3  # Only image files
        assert data["total"] == 3
        
        # Check that each item has required fields
        for item in data["items"]:
            assert "id" in item
            assert "filename" in item
            assert "uploadDate" in item
            assert "url" in item
            assert item["url"].startswith("/api/processed_uploads/")
    
    def test_list_images_pagination(self):
        """Test pagination functionality"""
        # Create multiple test images
        for i in range(5):
            self.create_test_image(f"test{i}.jpg")
        
        # Test first page with page_size=2
        response = client.get("/api/images?page=1&page_size=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 2
        
        # Test second page
        response = client.get("/api/images?page=2&page_size=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 2
        assert data["page"] == 2
    
    def test_delete_image_success(self):
        """Test successful image deletion"""
        # Create test images in both directories
        processed_file = self.create_test_image("test_image.jpg", self.test_uploads_dir)
        original_file = self.create_test_image("original_test_image.jpg", self.test_original_uploads_dir)
        
        # Test deletion
        response = client.delete("/api/images/test_image")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "processed_deleted" in data
        assert "original_deleted" in data
        assert "test_image" in data["message"]
    
    def test_delete_image_not_found(self):
        """Test deletion of non-existent image"""
        response = client.delete("/api/images/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_delete_image_processed_only(self):
        """Test deletion when only processed image exists"""
        processed_file = self.create_test_image("test_image.jpg", self.test_uploads_dir)
        
        response = client.delete("/api/images/test_image")
        assert response.status_code == 200
        
        data = response.json()
        assert data["processed_deleted"] == True
        assert data["original_deleted"] == False
        assert not processed_file.exists()
    
    def test_delete_image_original_only(self):
        """Test deletion when only original image exists"""
        original_file = self.create_test_image("test_image.jpg", self.test_original_uploads_dir)
        
        response = client.delete("/api/images/test_image")
        assert response.status_code == 200
        
        data = response.json()
        assert data["processed_deleted"] == False
        assert data["original_deleted"] == True
        assert not original_file.exists()
    
    def test_list_images_query_params_validation(self):
        """Test query parameter validation"""
        # Test invalid page (should default or handle gracefully)
        response = client.get("/api/images?page=0")
        assert response.status_code == 422  # Validation error
        
        # Test invalid page_size
        response = client.get("/api/images?page_size=0")
        assert response.status_code == 422  # Validation error
        
        # Test page_size too large
        response = client.get("/api/images?page_size=200")
        assert response.status_code == 422  # Validation error