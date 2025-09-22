from fastapi.testclient import TestClient
import pytest
from pathlib import Path
import shutil
from app.main import app
from datetime import datetime, timezone
import os

client = TestClient(app)

@pytest.fixture
def setup_test_uploads():
    # Create test uploads directory
    test_uploads = Path("uploads")
    test_uploads.mkdir(exist_ok=True)
    
    # Create some test image files
    for i in range(1, 4):
        test_file = test_uploads / f"test_image_{i}.jpg"
        test_file.touch()
    
    yield
    
    # Cleanup after tests
    shutil.rmtree(test_uploads)

def test_list_images_empty():
    response = client.get("/api/images")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    assert data["total"] == 0

def test_list_images_with_files(setup_test_uploads):
    response = client.get("/api/images")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 3
    assert data["total"] == 3
    
    # Check first item structure
    first_item = data["items"][0]
    assert "id" in first_item
    assert "filename" in first_item
    assert "uploadDate" in first_item
    assert "url" in first_item

def test_pagination(setup_test_uploads):
    # Test first page
    response = client.get("/api/images?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 2
    
    # Test second page
    response = client.get("/api/images?page=2&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 3
    assert data["page"] == 2

def test_invalid_pagination():
    # Test invalid page number
    response = client.get("/api/images?page=0")
    assert response.status_code == 422
    
    # Test invalid page size
    response = client.get("/api/images?page_size=0")
    assert response.status_code == 422
    response = client.get("/api/images?page_size=101")
    assert response.status_code == 422