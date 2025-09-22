Build a new "Uploaded Images List" feature.

Requirements:
- **Backend API**  
  - Create an endpoint `/api/images` that retrieves all uploaded images.  
  - Each image should return metadata: `id`, `filename`, `uploadDate`, `url`.  
  - Support pagination via query params: `page`, `pageSize`.  

- **Frontend Page/Component**  
  - Create a page `/images` that fetches from `/api/images`.  
  - Display images in a **responsive grid** (mobile & desktop).  
  - Each image card should show the thumbnail, filename, and upload date.  
  - Implement **lazy loading or pagination controls** if many images exist.  
  - Ensure responsive design with CSS grid or flexbox.  

- **Testing**  
  - Add unit tests for the backend API (mock storage/database).  
  - Add frontend tests to ensure the list view displays images and metadata.  
  - Verify pagination/lazy loading works correctly.  

Acceptance Criteria:
[X] All uploaded images are visible in the list view.  
[X] Page works across devices and browsers.  
[X] Tests cover the main flows (fetching, rendering, pagination).  