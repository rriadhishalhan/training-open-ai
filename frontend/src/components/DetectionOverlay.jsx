import { useEffect, useRef, useState } from 'react'

/**
 * DetectionOverlay component that renders bounding boxes with labels over an image
 * @param {Object} props
 * @param {string} props.imageUrl - URL of the image to display
 * @param {Array} props.boxes - Array of bounding box objects with label, x, y, w, h, score
 * @returns {JSX.Element}
 */
function DetectionOverlay({ imageUrl, boxes = [] }) {
    const [containerSize, setContainerSize] = useState({ width: 0, height: 0 })
    const [imageSize, setImageSize] = useState({ width: 0, height: 0 })
    const [imageLoaded, setImageLoaded] = useState(false)
    const containerRef = useRef(null)

    // Handle image load to get actual dimensions
    const handleImageLoad = (event) => {
        const img = event.target
        setImageSize({ width: img.naturalWidth, height: img.naturalHeight })

        // Also get container size (displayed image size)
        setContainerSize({ width: img.offsetWidth, height: img.offsetHeight })
        setImageLoaded(true)
    }

    // Reset state when imageUrl changes
    useEffect(() => {
        setImageLoaded(false)
        setImageSize({ width: 0, height: 0 })
        setContainerSize({ width: 0, height: 0 })
    }, [imageUrl])

    return (
        <div ref={containerRef} className="relative inline-block">
            {/* Main image */}
            <img
                src={imageUrl}
                alt="Uploaded image with object detection"
                className="max-w-full h-auto block"
                onLoad={handleImageLoad}
                onError={() => setImageLoaded(false)}
            />

            {/* Overlay container for bounding boxes */}
            {imageLoaded && boxes.length > 0 && containerSize.width > 0 && (
                <div className="absolute inset-0">
                    {boxes.map((box, index) => {
                        // Scale factors from original image to displayed image
                        const scaleX = containerSize.width / imageSize.width
                        const scaleY = containerSize.height / imageSize.height

                        // Convert absolute coordinates to pixels on displayed image
                        const left = box.x * scaleX
                        const top = box.y * scaleY
                        const width = box.w * scaleX
                        const height = box.h * scaleY

                        return (
                            <div
                                key={index}
                                className="absolute border-2 border-red-500 bg-red-500/10"
                                style={{
                                    left: `${left}px`,
                                    top: `${top}px`,
                                    width: `${width}px`,
                                    height: `${height}px`,
                                }}
                            >
                                {/* Label with confidence score */}
                                <div className="absolute -top-6 left-0 bg-red-500 text-white px-2 py-1 text-xs rounded whitespace-nowrap">
                                    {box.label} ({Math.round(box.score * 100)}%)
                                </div>
                            </div>
                        )
                    })}
                </div>
            )}

            {/* Loading state when image is loading */}
            {!imageLoaded && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-100/80">
                    <div className="text-sm text-gray-600">Loading image...</div>
                </div>
            )}

            {/* Info text when no boxes detected */}
            {imageLoaded && boxes.length === 0 && (
                <div className="absolute bottom-2 left-2 bg-black/70 text-white px-2 py-1 text-xs rounded">
                    No objects detected
                </div>
            )}
        </div>
    )
}

export default DetectionOverlay