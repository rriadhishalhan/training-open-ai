import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import { Toaster } from './components/ui/toaster'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import { ImagesPage } from './pages/ImagesPage'

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/images" element={<ImagesPage />} />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </>
  )
}

export default App
