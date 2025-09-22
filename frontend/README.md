# Frontend - Image Upload App

A modern React application built with Vite, Tailwind CSS, and shadcn/ui for uploading images to a FastAPI backend.

## Environment Setup

### Prerequisites

- Node.js (v18+ recommended)
- npm or yarn

### Environment Variables

Create a `.env` file in the frontend directory with the following configuration:

```env
VITE_API_BASE_URL=http://localhost:8000
```

This tells the frontend where to find the FastAPI backend service.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

### 4. Preview Production Build

```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Features

- ✅ Modern, responsive UI with Tailwind CSS and shadcn/ui
- ✅ Multiple image file selection
- ✅ Drag-and-drop file upload with visual feedback
- ✅ Image preview thumbnails
- ✅ Real-time upload progress
- ✅ File validation (images only)
- ✅ Keyboard accessibility
- ✅ Toast notifications for success/error feedback
- ✅ Clean, centered card layout
- ✅ Image gallery with pagination
- ✅ Image deletion with confirmation dialog
- ✅ Bulk image selection and deletion
- ✅ Object detection visualization

## Architecture

### Tech Stack

- **React** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern component library
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

### Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── ui/          # shadcn/ui components + custom components
│   │       ├── button.jsx
│   │       ├── input.jsx
│   │       ├── progress.jsx
│   │       ├── page-header.jsx
│   │       ├── confirmation-modal.jsx  # Image deletion confirmation
│   │       ├── toaster.jsx
│   │       └── use-toast.js
│   ├── lib/             # Utilities and API helpers
│   │   ├── api.js       # API functions (upload, list, delete images)
│   │   └── utils.js
│   ├── pages/           # React Router pages
│   │   ├── HomePage.jsx
│   │   ├── UploadPage.jsx
│   │   ├── ImagesPage.jsx     # Image gallery with deletion
│   │   └── ImagesPage.test.jsx # Tests for ImagesPage
│   └── assets/          # Static assets
├── public/              # Public static files
└── package.json
```

## API Integration

The frontend communicates with the FastAPI backend via:

- **GET /health** - Health check endpoint
- **POST /api/upload** - File upload endpoint (multipart/form-data)
- **GET /api/images** - List uploaded images with pagination
- **DELETE /api/images/{id}** - Delete specific image by ID
- **GET /api/detections/{image_id}** - Get object detection results

Upload requests send files as `files[]` in multipart form data format.

## Accessibility Features

- ✅ Proper ARIA labels and descriptions
- ✅ Keyboard navigation support
- ✅ Focus indicators on interactive elements
- ✅ Screen reader compatible
- ✅ Semantic HTML structure
- ✅ Progress bar with proper role and attributes

## Troubleshooting

### Common Issues

1. **Backend connection errors**
   - Ensure `VITE_API_BASE_URL` is set correctly
   - Verify the backend is running on the specified port

2. **Build errors**
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
   - Check Node.js version compatibility

3. **Styling issues**
   - Ensure Tailwind CSS is configured properly
   - Check that all shadcn/ui components are imported correctly

## Acceptance Checklist

### Task 1.4.3 - Styling, Accessibility & README

- [x] **Modern, clean page consistent with Tailwind + shadcn/ui**
  - Centered card layout with max-width
  - Proper padding and rounded corners
  - Subtle shadow effects
  - Gradient background
  - Consistent spacing and typography

- [x] **Keyboard navigation and focus states verified; inputs labeled**
  - Visible focus rings on interactive elements
  - Proper ARIA labels and descriptions
  - Keyboard accessible file selection
  - Screen reader compatible file list
  - Progress bar with proper accessibility attributes

- [x] **frontend/README.md includes env config and acceptance checklist**
  - Environment setup instructions
  - VITE_API_BASE_URL configuration
  - Quick-start commands
  - Complete acceptance checklist
  - Architecture documentation
  - Troubleshooting guide

- [x] **(Optional) Drag-and-drop with previews works without breaking basic flow**
  - Drag-and-drop zone with visual feedback
  - Image preview thumbnails in file list
  - Automatic preview cleanup for memory management

### Overall Acceptance (cross-task)

- [x] **`/upload` page exists and is reachable**
- [x] **Users can select and upload one or multiple images**
- [x] **Uploads hit backend and show progress + success/failure feedback**
- [x] **Page uses shadcn/ui components and app is bootstrapped with Vite under `frontend/`**

## Next Steps

1. Consider implementing drag-and-drop functionality
2. Add image preview thumbnails
3. Implement file removal before upload
4. Add upload queue management for large batches
