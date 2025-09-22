# Bootcamp Day 1 - Monorepo Project

A modern full-stack application with FastAPI backend and React frontend, designed for learning modern web development practices.

## Project Structure

```
.
├── backend/                 # FastAPI service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   └── routes/         # API endpoints
│   │       ├── __init__.py
│   │       ├── health.py   # Health check endpoint
│   │       └── upload.py   # File upload endpoint
│   ├── pyproject.toml      # Python dependencies (uv)
│   └── README.md           # Backend documentation
├── frontend/               # React application (placeholder)
│   └── README.md           # Frontend documentation
├── note-day1.md           # Lab instructions
├── note-day2.md           # Additional notes
└── README.md              # This file
```

## Features

### Backend (FastAPI)
- ✅ **Health Check**: `GET /api/health` - Service health monitoring
- 📁 **File Upload**: `POST /api/upload` - Multi-file upload with metadata
- 📚 **Interactive Docs**: Swagger UI and ReDoc documentation
- 🚀 **Modern Tools**: uv for dependency management, automatic reload
- 🌐 **CORS Ready**: Configured for frontend integration

### Frontend (Planned)
- ⚛️ **React + Vite**: Modern development experience
- 🎨 **Tailwind CSS**: Utility-first styling
- 🧩 **shadcn/ui**: Beautiful, accessible components
- 📤 **File Upload UI**: Drag-and-drop interface with progress tracking

## Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Start the development server:**
   ```bash
   uv run dev
   ```

5. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/health

### Frontend Setup

The frontend is currently a placeholder. Follow the instructions in `note-day1.md` to implement the React application.

## API Endpoints

| Method | Endpoint      | Description                    | Status |
|--------|---------------|--------------------------------|---------|
| GET    | `/`           | Root endpoint with API info   | ✅      |
| GET    | `/api/health` | Health check                   | ✅      |
| POST   | `/api/upload` | File upload (multipart)       | ✅      |
| GET    | `/docs`       | Swagger UI documentation       | ✅      |
| GET    | `/redoc`      | ReDoc documentation           | ✅      |

## Development Workflow

1. **Backend Development:**
   ```bash
   cd backend
   uv run dev  # Starts with auto-reload
   ```

2. **Frontend Development:** (to be implemented)
   ```bash
   cd frontend
   npm run dev  # Will start Vite dev server
   ```

3. **Full Stack Testing:**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000 or http://localhost:5173

## Testing the Upload Endpoint

### Using curl:
```bash
curl -X POST "http://localhost:8000/api/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@path/to/your/file.jpg"
```

### Using the Swagger UI:
1. Go to http://localhost:8000/docs
2. Find the `/api/upload` endpoint
3. Click "Try it out"
4. Choose files to upload
5. Click "Execute"

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **uvicorn**: ASGI server for FastAPI
- **python-multipart**: File upload support
- **uv**: Ultra-fast Python package manager

### Frontend (Planned)
- **React**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Component library
- **axios**: HTTP client for API calls

## Next Steps

1. ✅ Backend FastAPI service with health and upload endpoints
2. 🔄 Frontend React application setup
3. 🔄 File upload UI with progress tracking
4. 🔄 Error handling and validation
5. 🔄 Testing and documentation

## Contributing

This project is part of a bootcamp curriculum. Follow the lab instructions in `note-day1.md` for guided development.

## Troubleshooting

### Backend Issues
- **Port 8000 in use**: Stop other services or change port in the command
- **Import errors**: Ensure you're in the `backend/` directory and ran `uv sync`
- **uv not found**: Install uv following the instructions above

### CORS Issues
- The backend is configured for `localhost:3000` and `localhost:5173`
- Modify CORS settings in `backend/app/main.py` if using different ports

For detailed troubleshooting, see `backend/README.md`.

---

## Original Development Container Info

This workspace is set up with:
- **Python 3.12** development container
- **Node.js** and **SQLite** via devcontainer features
- **UV** package manager for fast Python package management
- **GitHub Copilot** integration
- **Port forwarding** for development (3000, 5173, 8000)

SQLite is pre-installed and ready to use:

```bash
# Open SQLite command line
sqlite3 database.db

# Check SQLite version
sqlite3 --version
```

### Node.js

Node.js and npm are available for frontend development:

```bash
# Check versions
node --version
npm --version

# Install packages
npm install package_name
```

## Port Forwarding

The following ports are automatically forwarded:
- **3000**: Common for React/Next.js development servers
- **5173**: Vite development server default port
- **8000**: Common for Python web servers (Django, FastAPI, etc.)

## VS Code Extensions

The container comes pre-configured with essential development extensions:

### 🤖 AI & Productivity
- **GitHub Copilot**: AI-powered code suggestions and completion

### 🐍 Python Development
- **Python**: Core Python language support and debugging
- **Pylance**: Fast, feature-rich Python language server
- **Black Formatter**: Opinionated Python code formatter
- **isort**: Import statement organizer
- **Flake8**: Python linting and code quality checking

### 🛠️ General Development
- **JSON**: Enhanced JSON language support
- **Tailwind CSS**: CSS framework IntelliSense (useful for web development)

## Configuration Features

### 🔧 Automatic Code Formatting
- **Format on Save**: Enabled
- **Import Organization**: Automatic with isort
- **Black Integration**: Consistent Python code styling

### 🚀 Development Workflow
- **Python Interpreter**: Pre-configured at `/usr/local/bin/python`
- **Linting**: Flake8 enabled for code quality
- **Debugging**: Full debugging support with breakpoints and variable inspection

## Example Usage

Create a simple Python web server:

```python
# app.py
from http.server import HTTPServer, SimpleHTTPRequestHandler

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
```

Run it:
```bash
python app.py
```

The server will be accessible at `http://localhost:8000` thanks to port forwarding.
