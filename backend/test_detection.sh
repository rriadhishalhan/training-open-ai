#!/bin/bash

# Test script for Azure Computer Vision Object Detection endpoint
# This script demonstrates the /detections/{id} endpoint functionality

echo "=== Testing Azure Computer Vision Object Detection Endpoint ==="
echo

# Test 1: Check if server is running
echo "1. Testing server health..."
curl -s -X GET "http://localhost:8000/api/health" | jq .
echo

# Test 2: Upload a test image
echo "2. Uploading test image..."
UPLOAD_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/upload" \
  -F "files[]=@/workspaces/bootcamp-day1/frontend/public/vite.svg")
echo $UPLOAD_RESPONSE | jq .

# Extract the saved filename
SAVED_FILENAME=$(echo $UPLOAD_RESPONSE | jq -r '.files[0].saved_filename')
echo "Saved filename: $SAVED_FILENAME"
echo

# Test 3: Test detection endpoint with missing Azure credentials (expected to fail gracefully)
echo "3. Testing detection endpoint (without Azure credentials - should fail gracefully)..."
curl -s -X GET "http://localhost:8000/api/detections/$SAVED_FILENAME" | jq .
echo

# Test 4: Test detection endpoint with non-existent image
echo "4. Testing detection endpoint with non-existent image..."
curl -s -X GET "http://localhost:8000/api/detections/non-existent-image.jpg" | jq .
echo

echo "=== Test Complete ==="
echo
echo "To test with actual Azure Computer Vision:"
echo "1. Set environment variables:"
echo "   export VISION_ENDPOINT='https://your-vision-service.cognitiveservices.azure.com/'"
echo "   export VISION_KEY='your-api-key'"
echo "2. Restart the server"
echo "3. Run: curl -X GET \"http://localhost:8000/api/detections/$SAVED_FILENAME\""