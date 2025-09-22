import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { vi } from 'vitest'
import { ImagesPage } from './ImagesPage'
import { listImages, deleteImage } from '../lib/api'

// Mock the API module
vi.mock('../lib/api', () => ({
    listImages: vi.fn(),
    deleteImage: vi.fn()
}))

// Mock react-hot-toast
vi.mock('../components/ui/use-toast', () => ({
    toast: {
        success: vi.fn(),
        error: vi.fn()
    }
}))

const mockImages = {
    items: [
        {
            id: '1',
            filename: 'test1.jpg',
            uploadDate: '2025-09-18T10:00:00Z',
            url: '/uploads/test1.jpg'
        },
        {
            id: '2',
            filename: 'test2.jpg',
            uploadDate: '2025-09-18T09:00:00Z',
            url: '/uploads/test2.jpg'
        }
    ],
    total: 2,
    page: 1,
    page_size: 12
}

describe('ImagesPage', () => {
    beforeEach(() => {
        listImages.mockReset()
        deleteImage.mockReset()
    })

    it('renders loading state initially', () => {
        listImages.mockImplementation(() => new Promise(() => {}))
        render(<ImagesPage />)
        expect(screen.getByRole('status')).toBeInTheDocument()
    })

    it('displays images when loaded', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        render(<ImagesPage />)

        await waitFor(() => {
            expect(screen.getByText('test1.jpg')).toBeInTheDocument()
            expect(screen.getByText('test2.jpg')).toBeInTheDocument()
        })
    })

    it('shows error message when API fails', async () => {
        listImages.mockRejectedValueOnce(new Error('API Error'))
        render(<ImagesPage />)

        await waitFor(() => {
            expect(screen.getByText('Failed to load images')).toBeInTheDocument()
        })
    })

    it('shows empty state when no images', async () => {
        listImages.mockResolvedValueOnce({
            items: [],
            total: 0,
            page: 1,
            page_size: 12
        })
        render(<ImagesPage />)

        await waitFor(() => {
            expect(screen.getByText('No images uploaded yet')).toBeInTheDocument()
        })
    })

    it('handles pagination correctly', async () => {
        // Mock first page
        listImages.mockResolvedValueOnce({
            ...mockImages,
            total: 24 // 2 pages
        })

        render(<ImagesPage />)

        await waitFor(() => {
            expect(screen.getByText('Page 1 of 2')).toBeInTheDocument()
        })

        // Mock second page data
        listImages.mockResolvedValueOnce({
            ...mockImages,
            page: 2,
            total: 24
        })

        // Click next page
        fireEvent.click(screen.getByText('Next'))

        await waitFor(() => {
            expect(screen.getByText('Page 2 of 2')).toBeInTheDocument()
        })
    })

    it('shows delete button on each image when not in selection mode', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        render(<ImagesPage />)

        await waitFor(() => {
            const deleteButtons = screen.getAllByText('×')
            expect(deleteButtons).toHaveLength(2) // One for each image
        })
    })

    it('opens confirmation modal when delete button is clicked', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        render(<ImagesPage />)

        await waitFor(() => {
            const deleteButtons = screen.getAllByText('×')
            fireEvent.click(deleteButtons[0])
        })

        await waitFor(() => {
            expect(screen.getByText('Delete Image')).toBeInTheDocument()
            expect(screen.getByText(/Are you sure you want to delete "test1.jpg"/)).toBeInTheDocument()
        })
    })

    it('deletes image when confirmation is confirmed', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        deleteImage.mockResolvedValueOnce({ message: 'Image deleted successfully' })
        
        // Mock the second call to listImages after deletion
        listImages.mockResolvedValueOnce({
            items: [mockImages.items[1]], // Only second image remains
            total: 1,
            page: 1,
            page_size: 12
        })

        render(<ImagesPage />)

        await waitFor(() => {
            const deleteButtons = screen.getAllByText('×')
            fireEvent.click(deleteButtons[0])
        })

        await waitFor(() => {
            const confirmButton = screen.getByText('Delete')
            fireEvent.click(confirmButton)
        })

        await waitFor(() => {
            expect(deleteImage).toHaveBeenCalledWith('1')
        })
    })

    it('toggles selection mode when Select Images button is clicked', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        render(<ImagesPage />)

        await waitFor(() => {
            const selectButton = screen.getByText('Select Images')
            fireEvent.click(selectButton)
        })

        await waitFor(() => {
            expect(screen.getByText('Cancel Selection')).toBeInTheDocument()
            expect(screen.getAllByRole('checkbox')).toHaveLength(2)
        })
    })

    it('shows delete selected button when images are selected', async () => {
        listImages.mockResolvedValueOnce(mockImages)
        render(<ImagesPage />)

        // Enter selection mode
        await waitFor(() => {
            const selectButton = screen.getByText('Select Images')
            fireEvent.click(selectButton)
        })

        // Select an image
        await waitFor(() => {
            const checkboxes = screen.getAllByRole('checkbox')
            fireEvent.click(checkboxes[0])
        })

        await waitFor(() => {
            expect(screen.getByText('Delete Selected (1)')).toBeInTheDocument()
        })
    })
})