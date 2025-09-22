import { useState, useEffect } from 'react';
import { listImages, deleteImage } from '../lib/api';
import { Button } from '../components/ui/button';
import { PageHeader } from '../components/ui/page-header';
import { ConfirmationModal } from '../components/ui/confirmation-modal';
import { toast } from '../components/ui/use-toast';

export function ImagesPage() {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [pageSize] = useState(12); // Show 12 images per page
    const [selectedImages, setSelectedImages] = useState(new Set());
    const [isSelectionMode, setIsSelectionMode] = useState(false);
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [imageToDelete, setImageToDelete] = useState(null);
    const [isDeleting, setIsDeleting] = useState(false);

    useEffect(() => {
        fetchImages();
    }, [page]);

    const fetchImages = async () => {
        try {
            setLoading(true);
            const data = await listImages(page, pageSize);
            setImages(data.items);
            setTotalPages(Math.ceil(data.total / pageSize));
        } catch (err) {
            setError('Failed to load images');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteClick = (image) => {
        setImageToDelete(image);
        setShowConfirmModal(true);
    };

    const handleConfirmDelete = async () => {
        if (!imageToDelete) return;

        try {
            setIsDeleting(true);
            await deleteImage(imageToDelete.id);
            toast.success(`Image "${imageToDelete.filename}" deleted successfully`);
            
            // Refresh the images list
            await fetchImages();
            
            // Reset selection if the deleted image was selected
            setSelectedImages(prev => {
                const newSet = new Set(prev);
                newSet.delete(imageToDelete.id);
                return newSet;
            });
        } catch (err) {
            toast.error(`Failed to delete image: ${err.message}`);
            console.error(err);
        } finally {
            setIsDeleting(false);
            setShowConfirmModal(false);
            setImageToDelete(null);
        }
    };

    const handleCancelDelete = () => {
        setShowConfirmModal(false);
        setImageToDelete(null);
    };

    const toggleSelectionMode = () => {
        setIsSelectionMode(prev => !prev);
        setSelectedImages(new Set());
    };

    const toggleImageSelection = (imageId) => {
        setSelectedImages(prev => {
            const newSet = new Set(prev);
            if (newSet.has(imageId)) {
                newSet.delete(imageId);
            } else {
                newSet.add(imageId);
            }
            return newSet;
        });
    };

    const handleDeleteSelected = () => {
        if (selectedImages.size === 0) return;
        
        // For multiple deletions, we'll delete them one by one
        // In a real app, you might want a bulk delete API endpoint
        const firstImageId = Array.from(selectedImages)[0];
        const imageToDelete = images.find(img => img.id === firstImageId);
        if (imageToDelete) {
            setImageToDelete(imageToDelete);
            setShowConfirmModal(true);
        }
    };

    const formatDate = (isoDate) => {
        return new Date(isoDate).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="container mx-auto p-4">
            <PageHeader title="Uploaded Images" />
            
            {/* Action buttons */}
            <div className="flex gap-2 mb-4">
                <Button
                    variant="outline"
                    onClick={toggleSelectionMode}
                >
                    {isSelectionMode ? 'Cancel Selection' : 'Select Images'}
                </Button>
                {isSelectionMode && selectedImages.size > 0 && (
                    <Button
                        variant="destructive"
                        onClick={handleDeleteSelected}
                    >
                        Delete Selected ({selectedImages.size})
                    </Button>
                )}
            </div>
            
            {error && (
                <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
                    {error}
                </div>
            )}
            
            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                </div>
            ) : (
                <>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                        {images.map((image) => (
                            <div 
                                key={image.id} 
                                className={`bg-white rounded-lg shadow overflow-hidden relative ${
                                    isSelectionMode ? 'cursor-pointer' : ''
                                } ${
                                    selectedImages.has(image.id) ? 'ring-2 ring-blue-500' : ''
                                }`}
                                onClick={isSelectionMode ? () => toggleImageSelection(image.id) : undefined}
                            >
                                {/* Selection checkbox */}
                                {isSelectionMode && (
                                    <div className="absolute top-2 left-2 z-10">
                                        <input
                                            type="checkbox"
                                            checked={selectedImages.has(image.id)}
                                            onChange={() => toggleImageSelection(image.id)}
                                            className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded"
                                        />
                                    </div>
                                )}
                                
                                {/* Delete button for individual image */}
                                {!isSelectionMode && (
                                    <div className="absolute top-2 right-2 z-10">
                                        <Button
                                            size="sm"
                                            variant="destructive"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleDeleteClick(image);
                                            }}
                                            className="h-8 w-8 p-0"
                                        >
                                            ×
                                        </Button>
                                    </div>
                                )}
                                
                                <div className="aspect-w-1 aspect-h-1">
                                    <img
                                        src={image.url}
                                        alt={image.filename}
                                        className="object-cover w-full h-full"
                                        loading="lazy"
                                    />
                                </div>
                                <div className="p-4">
                                    <p className="font-medium text-gray-900 truncate">{image.filename}</p>
                                    <p className="text-sm text-gray-500">{formatDate(image.uploadDate)}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                    
                    {totalPages > 1 && (
                        <div className="flex justify-center gap-2 mt-8">
                            <Button
                                variant="outline"
                                onClick={() => setPage(p => Math.max(1, p - 1))}
                                disabled={page === 1}
                            >
                                Previous
                            </Button>
                            <span className="flex items-center px-4">
                                Page {page} of {totalPages}
                            </span>
                            <Button
                                variant="outline"
                                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                                disabled={page === totalPages}
                            >
                                Next
                            </Button>
                        </div>
                    )}
                    
                    {images.length === 0 && (
                        <div className="text-center text-gray-500 py-12">
                            No images uploaded yet
                        </div>
                    )}
                </>
            )}
            
            {/* Confirmation Modal */}
            <ConfirmationModal
                isOpen={showConfirmModal}
                onClose={handleCancelDelete}
                onConfirm={handleConfirmDelete}
                title="Delete Image"
                message={`Are you sure you want to delete "${imageToDelete?.filename}"? This action cannot be undone.`}
                confirmText="Delete"
                cancelText="Cancel"
                isLoading={isDeleting}
            />
        </div>
    );
}