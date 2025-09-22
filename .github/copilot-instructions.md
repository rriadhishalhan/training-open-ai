# GitHub Copilot Instructions for AI Coding Agents

## Project Overview
- **Monorepo** with FastAPI backend (`backend/`) and React frontend (`frontend/`)
- Designed for bootcamp learning; follow `note-day1.md` for guided development
- Backend exposes health, upload, image listing/deletion, and object detection endpoints
- Frontend implements file upload UI, image gallery, and object detection visualization

## Architecture & Key Patterns
- **Backend**: FastAPI app in `backend/app/main.py`, routes in `backend/app/routes/`
  - Endpoints: `/api/health`, `/api/upload`, `/api/images`, `/api/detections/{image_id}`
  - CORS configured for `localhost:3000` and `localhost:5173` (edit in `main.py`)
  - Uploaded files stored in `backend/uploads/`, processed images in `backend/processed_uploads/`
  - Object detection uses Azure Computer Vision (requires `VISION_ENDPOINT` and `VISION_KEY`)
- **Frontend**: React + Vite in `frontend/`, UI in `src/components/ui/`, API helpers in `src/lib/api.js`
  - Uses Tailwind CSS and shadcn/ui for styling and components
  - API base URL set via `.env` (`VITE_API_BASE_URL`)
  - Pages: `HomePage.jsx`, `UploadPage.jsx`, `ImagesPage.jsx`

## Developer Workflow
- **Backend**:
  - Install dependencies: `uv sync` (in `backend/`)
  - Start dev server: `uv run dev` or `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  - Run tests: `uv run pytest` (after `uv sync --dev`)
- **Frontend**:
  - Install dependencies: `npm install` (in `frontend/`)
  - Start dev server: `npm run dev` (default port 5173)
  - Build: `npm run build`; Preview: `npm run preview`

## Project-Specific Conventions
- **File Uploads**: Use `files[]` field in multipart form data for uploads
- **Pagination**: Image listing supports `page` and `page_size` query params
- **Error Handling**: API returns structured JSON with `message` and details
- **Accessibility**: Frontend enforces ARIA labels, keyboard navigation, and semantic HTML
- **Styling**: Use Tailwind and shadcn/ui; keep layouts centered, with max-width and gradients

## Integration Points
- **API communication**: All frontend API calls use `src/lib/api.js` (axios)
- **Object detection**: Backend integrates with Azure Computer Vision; set credentials via env vars
- **CORS**: Update allowed origins in `backend/app/main.py` if frontend port changes

## Examples
- **Backend health check**: `GET /api/health` returns `{"status": "ok"}`
- **Upload images**: `POST /api/upload` with `files[]` form field
- **Delete image**: `DELETE /api/images/{id}`
- **Frontend API usage**: See `src/lib/api.js` for request patterns

## References
- See `README.md` in project root, `backend/`, and `frontend/` for more details
- Lab instructions: `note-day1.md`
- Troubleshooting: `backend/README.md`, `frontend/README.md`

---

If any section is unclear or missing, please provide feedback for improvement.
