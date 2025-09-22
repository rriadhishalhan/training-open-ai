# AI Object Detection - Full Stack Application

A modern full-stack application with FastAPI backend and React frontend, featuring image upload, object detection using Azure Computer Vision, and interactive image management.

## Project Structure

```
.
├── backend/                        # FastAPI service
│   ├── app/
│   │   ├── main.py                # FastAPI application
│   │   ├── routes/                # API endpoints
│   │   │   ├── health.py          # Health check endpoint
│   │   │   ├── upload.py          # File upload endpoint
│   │   │   ├── images.py          # Image management (list/delete)
│   │   │   └── detection.py       # Azure Computer Vision integration
│   │   └── utils/
│   │       └── image_processing.py # Image processing utilities
│   ├── tests/                     # Backend tests
│   ├── uploads/                   # Original uploaded images
│   ├── processed_uploads/         # Images with detection overlays
│   ├── pyproject.toml            # Python dependencies (uv)
│   └── README.md                 # Backend documentation
├── frontend/                      # React + Vite application
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── ui/              # shadcn/ui components
│   │   │   └── DetectionOverlay.jsx # Object detection visualization
│   │   ├── pages/               # Application pages
│   │   │   ├── HomePage.jsx     # Landing page
│   │   │   ├── UploadPage.jsx   # File upload interface
│   │   │   └── ImagesPage.jsx   # Image gallery with detection
│   │   └── lib/
│   │       └── api.js           # API client helpers
│   ├── package.json             # Node.js dependencies
│   └── README.md               # Frontend documentation
├── docker-compose.yml           # Docker containerization
├── note-day1.md                # Lab instructions - Day 1
├── note-day2.md                # Lab instructions - Day 2
└── README.md                   # This file
```

## Features

### Backend (FastAPI) ✅ Complete
- ✅ **Health Check**: `GET /api/health` - Service health monitoring
- ✅ **File Upload**: `POST /api/upload` - Multi-file upload with metadata and validation
- ✅ **Image Management**: `GET /api/images` - Paginated image listing with metadata
- ✅ **Image Deletion**: `DELETE /api/images/{id}` - Remove images and cleanup
- ✅ **Object Detection**: `GET /api/detections/{id}` - Azure Computer Vision integration
- ✅ **Static File Serving**: Serves uploaded and processed images
- ✅ **Interactive Docs**: Swagger UI and ReDoc documentation
- ✅ **CORS Configuration**: Ready for frontend integration
- ✅ **Environment Configuration**: Azure Computer Vision API integration
- ✅ **Error Handling**: Comprehensive error responses and logging
- ✅ **Testing**: Unit tests for core functionality

### Frontend (React + Vite) ✅ Complete
- ✅ **React Router**: Multi-page navigation (Home, Upload, Images)
- ✅ **File Upload UI**: Drag-and-drop interface with progress tracking
- ✅ **Image Gallery**: Paginated display of uploaded images
- ✅ **Object Detection**: Interactive visualization of detected objects
- ✅ **Responsive Design**: Tailwind CSS with mobile-first approach
- ✅ **Component Library**: shadcn/ui for consistent, accessible UI
- ✅ **API Integration**: Axios-based client with error handling
- ✅ **Toast Notifications**: User feedback for all operations
- ✅ **Image Management**: Delete functionality with confirmation
- ✅ **Environment Configuration**: Configurable API base URL

### Infrastructure ✅ Complete
- ✅ **Docker Support**: Multi-stage builds for both services
- ✅ **Docker Compose**: Full-stack deployment with networking
- ✅ **Health Checks**: Container health monitoring
- ✅ **Volume Persistence**: Uploaded images persist across restarts
- ✅ **Environment Variables**: Configurable Azure API credentials
- ✅ **Nginx Proxy**: Production-ready frontend serving

## Quick Start

### Prerequisites
- **Python 3.12+** with uv package manager
- **Node.js 18+** with npm
- **Azure Computer Vision API** credentials (for object detection)
- **Docker & Docker Compose** (optional, for containerized deployment)

### Development Setup

#### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Install uv** (if not already installed):
   ```powershell
   # Windows PowerShell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies:**
   ```powershell
   uv sync
   ```

4. **Configure environment variables** (create `.env` file in project root):
   ```env
   # Azure Computer Vision API (required for object detection)
   VISION_ENDPOINT=https://your-vision-resource.cognitiveservices.azure.com/
   VISION_KEY=your-api-key-here
   
   # Optional: Azure OpenAI (for future features)
   AOAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
   AOAI_KEY=your-openai-key-here
   ```

5. **Start the development server:**
   ```powershell
   uv run dev
   ```

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Configure environment** (create `.env` file in frontend directory):
   ```env
   # API configuration (optional, defaults to relative URLs)
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Start the development server:**
   ```powershell
   npm run dev
   ```

### Docker Deployment

1. **Configure environment variables** (create `.env` file in project root):
   ```env
   # Azure Computer Vision API
   VISION_ENDPOINT=https://your-vision-resource.cognitiveservices.azure.com/
   VISION_KEY=your-api-key-here
   
   # Frontend API configuration (leave empty for production)
   VITE_API_BASE_URL=
   BACKEND_HOST=backend
   ```

2. **Start all services:**
   ```powershell
   docker-compose up --build
   ```

### Access the Application

- **Frontend**: http://localhost:3000 (Docker) or http://localhost:5173 (dev)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## API Endpoints

| Method | Endpoint                     | Description                           | Status |
|--------|------------------------------|---------------------------------------|---------|
| GET    | `/`                          | Root endpoint with API info          | ✅      |
| GET    | `/api/health`                | Health check                          | ✅      |
| POST   | `/api/upload`                | Multi-file upload (multipart)        | ✅      |
| GET    | `/api/images`                | List uploaded images (paginated)     | ✅      |
| DELETE | `/api/images/{id}`           | Delete image by ID                    | ✅      |
| GET    | `/api/detections/{id}`       | Object detection analysis             | ✅      |
| GET    | `/api/detections/{id}/image` | Get image with detection overlays     | ✅      |
| GET    | `/api/uploads/{filename}`    | Serve original uploaded files         | ✅      |
| GET    | `/api/processed_uploads/{filename}` | Serve processed images        | ✅      |
| GET    | `/docs`                      | Swagger UI documentation              | ✅      |
| GET    | `/redoc`                     | ReDoc documentation                   | ✅      |

### API Usage Examples

#### Upload Images
```powershell
# Upload single image
curl -X POST "http://localhost:8000/api/upload" `
     -H "Content-Type: multipart/form-data" `
     -F "files[]=@path/to/image.jpg"

# Upload multiple images
curl -X POST "http://localhost:8000/api/upload" `
     -H "Content-Type: multipart/form-data" `
     -F "files[]=@image1.jpg" `
     -F "files[]=@image2.jpg"
```

#### List Images
```powershell
# Get first page (10 items)
curl "http://localhost:8000/api/images"

# Get specific page with custom page size
curl "http://localhost:8000/api/images?page=2&page_size=5"
```

#### Object Detection
```powershell
# Analyze image and get processed image URL
curl "http://localhost:8000/api/detections/your-image-id.jpg"

# Get image with detection overlays directly
curl "http://localhost:8000/api/detections/your-image-id.jpg/image" -o processed_image.jpg
```

#### Delete Image
```powershell
curl -X DELETE "http://localhost:8000/api/images/your-image-id"
```

## Development Workflow

### Backend Development
```powershell
cd backend
uv run dev  # Starts FastAPI with auto-reload on port 8000
```

### Frontend Development
```powershell
cd frontend
npm run dev  # Starts Vite dev server on port 5173
```

### Full Stack Testing
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173 (dev) or http://localhost:3000 (Docker)
- **API Docs**: http://localhost:8000/docs

### Testing
```powershell
# Backend tests
cd backend
uv run pytest

# Frontend tests (if configured)
cd frontend
npm test
```

### Building for Production
```powershell
# Backend (uv handles Python packaging)
cd backend
uv build

# Frontend
cd frontend
npm run build
npm run preview  # Preview production build
```

## Application Features

### Image Upload
- **Drag & Drop Interface**: Modern file upload with visual feedback
- **Multi-file Support**: Upload multiple images simultaneously
- **Progress Tracking**: Real-time upload progress indicators
- **File Validation**: Supported formats and size limits
- **Instant Preview**: Preview images before upload

### Object Detection
- **Azure Computer Vision**: Industry-standard object detection
- **Visual Overlays**: Bounding boxes with labels and confidence scores
- **Real-time Processing**: On-demand analysis of uploaded images
- **Detection Results**: Detailed object information and coordinates

### Image Management
- **Gallery View**: Responsive grid layout of all images
- **Pagination**: Efficient browsing of large image collections
- **Search & Filter**: Find images quickly (future enhancement)
- **Bulk Operations**: Select and delete multiple images
- **Metadata Display**: Upload dates, file sizes, and detection status

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs with automatic documentation
- **uvicorn**: High-performance ASGI server
- **python-multipart**: File upload support
- **httpx**: Async HTTP client for Azure API integration
- **Pillow (PIL)**: Image processing and manipulation
- **python-dotenv**: Environment variable management
- **uv**: Ultra-fast Python package manager and dependency resolver

### Frontend
- **React 19**: Latest React with concurrent features
- **Vite**: Lightning-fast build tool and dev server
- **React Router DOM**: Client-side routing and navigation
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality, accessible component library
- **Lucide React**: Beautiful icon library
- **axios**: HTTP client for API communication
- **react-hot-toast**: Toast notifications for user feedback

### Infrastructure & DevOps
- **Docker**: Containerization for consistent deployments
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Production-ready web server and reverse proxy
- **Multi-stage Builds**: Optimized Docker images
- **Health Checks**: Container monitoring and recovery

### Azure Services
- **Azure Computer Vision**: Object detection and image analysis
- **Azure OpenAI**: (Configured for future RAG functionality)
- **Azure AI Search**: (Configured for future search features)

## Project Status & Roadmap

### ✅ Completed Features
1. **Backend API**: Complete FastAPI service with all endpoints
2. **Frontend Application**: Full React SPA with routing and UI
3. **Object Detection**: Azure Computer Vision integration
4. **Image Management**: Upload, list, view, and delete functionality
5. **Docker Support**: Full containerization with docker-compose
6. **Documentation**: Comprehensive API docs and README
7. **Testing**: Basic test coverage for core functionality

### 🔄 Current Development
- Performance optimizations for large image uploads
- Enhanced error handling and validation
- Additional test coverage

### � Future Enhancements
- **RAG Integration**: Azure OpenAI for image analysis and Q&A
- **Search Functionality**: Azure AI Search for image content search
- **User Authentication**: Multi-user support with role-based access
- **Image Filtering**: Advanced filtering by detection results
- **Batch Processing**: Background job processing for large uploads
- **Analytics Dashboard**: Usage statistics and detection insights

## Contributing

This project is part of a bootcamp curriculum for learning modern full-stack development. 

### Learning Path
1. **Day 1**: Backend development with FastAPI (`note-day1.md`)
2. **Day 2**: Frontend development with React (`note-day2.md`)
3. **Additional Labs**: Advanced features and deployment

### Development Guidelines
- Follow the existing code structure and patterns
- Write tests for new functionality
- Update documentation when adding features
- Use the provided environment configuration
- Test both development and Docker deployment modes

## Troubleshooting

### Common Issues

#### Backend Issues
- **Port 8000 in use**: Stop other services or change port in startup command
- **Import errors**: Ensure you're in the `backend/` directory and ran `uv sync`
- **uv not found**: Install uv following the installation instructions
- **Azure API errors**: Verify `VISION_ENDPOINT` and `VISION_KEY` are correctly set in `.env`
- **File upload failures**: Check uploads directory permissions and disk space

#### Frontend Issues
- **Port 5173 in use**: Vite will automatically find the next available port
- **API connection errors**: Verify backend is running and `VITE_API_BASE_URL` is correct
- **Build failures**: Ensure all dependencies are installed with `npm install`
- **CORS errors**: Backend is configured for ports 3000, 5173, and 5174

#### Docker Issues
- **Container startup failures**: Check environment variables in `.env` file
- **Volume mount issues**: Ensure Docker has permission to access project directory
- **Network connectivity**: Verify containers can communicate through app-network
- **Health check failures**: Check backend service logs for API errors

### Debugging Tips
- **Backend logs**: Use `uv run dev` for detailed FastAPI logs
- **Frontend console**: Check browser developer tools for errors
- **Docker logs**: Use `docker-compose logs [service]` to view container logs
- **API testing**: Use `/docs` endpoint to test API calls interactively

For detailed troubleshooting guides, see:
- `backend/README.md` - Backend-specific issues
- `frontend/README.md` - Frontend-specific issues

---

## Development Container Information

This workspace is configured with a development container setup for immediate productivity:

### Pre-installed Tools
- **Python 3.12** development environment
- **Node.js & npm** for frontend development  
- **SQLite** database for local development
- **UV** package manager for Python dependencies
- **GitHub Copilot** AI coding assistance

### VS Code Extensions
- **Python Development**: Python, Pylance, Black Formatter, isort, Flake8
- **AI Assistance**: GitHub Copilot for code suggestions
- **Web Development**: JSON, Tailwind CSS IntelliSense
- **Code Quality**: Auto-formatting on save, integrated linting

### Port Forwarding
Development servers are automatically accessible:
- **3000**: React development server (production mode)
- **5173**: Vite development server (default)
- **8000**: FastAPI backend server

### Quick Database Setup
SQLite is ready to use for future database features:
```powershell
# Open SQLite command line
sqlite3 database.db

# Check version
sqlite3 --version
```

This setup ensures a consistent development environment across different machines and operating systems.
