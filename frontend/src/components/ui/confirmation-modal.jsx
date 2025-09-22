import { Button } from './button';

export function ConfirmationModal({ 
    isOpen, 
    onClose, 
    onConfirm, 
    title, 
    message, 
    confirmText = "Delete", 
    cancelText = "Cancel",
    isLoading = false 
}) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-md w-full p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {title}
                </h3>
                <p className="text-gray-600 mb-6">
                    {message}
                </p>
                <div className="flex gap-3 justify-end">
                    <Button
                        variant="outline"
                        onClick={onClose}
                        disabled={isLoading}
                    >
                        {cancelText}
                    </Button>
                    <Button
                        variant="destructive"
                        onClick={onConfirm}
                        disabled={isLoading}
                    >
                        {isLoading ? "Deleting..." : confirmText}
                    </Button>
                </div>
            </div>
        </div>
    );
}