Feature Request: Image List and Deletion

Overview:
Implement functionality to:
- List all available images.
- Delete selected images.

Requirements:
- Provide an API endpoint `/api/images` to retrieve a list of images.  
  - Each image should include: `id`, `filename`, `uploadDate`, `url`.  
- Provide an API endpoint `/api/images/{id}` to delete an image by ID.  
- Ensure safe deletion with a confirmation step on the frontend (e.g., modal or prompt).  
- Support deleting one or multiple images.  
- Update documentation to describe how to list and delete images.  

Acceptance Criteria:
[✅] Users can view all available images in a list or grid.  
[✅] Users can delete selected images.  
[✅] Deletion is confirmed before removal.  
[✅] Documentation clearly explains how to use listing and deletion features.  

Additional Notes:
- Add permission checks to ensure only authorized users can delete images.  
- Write unit tests and integration tests for listing and deletion.  
- Ensure frontend design is responsive (desktop & mobile).  