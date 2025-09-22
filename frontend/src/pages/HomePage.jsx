import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import reactLogo from '../assets/react.svg'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Progress } from '../components/ui/progress'
import { toast } from '../components/ui/use-toast'
import viteLogo from '/vite.svg'

function HomePage() {
    const [count, setCount] = useState(0)
    const [progress, setProgress] = useState(0)
    const [inputValue, setInputValue] = useState('')
    const navigate = useNavigate()

    const handleToast = () => {
        toast.success('This is a sample toast notification!')
    }

    const handleProgress = () => {
        setProgress(prev => prev >= 100 ? 0 : prev + 20)
    }

    const handleUploadNavigate = () => {
        navigate('/upload')
    }

    return (
        <div className="min-h-screen bg-background text-foreground">
            <div className="container mx-auto p-8">
                <div className="text-center mb-8">
                    <div className="flex justify-center items-center gap-4 mb-6">
                        <a href="https://vite.dev" target="_blank">
                            <img src={viteLogo} className="logo" alt="Vite logo" />
                        </a>
                        <a href="https://react.dev" target="_blank">
                            <img src={reactLogo} className="logo react" alt="React logo" />
                        </a>
                    </div>
                    <h1 className="text-4xl font-bold mb-4">Vite + React + Tailwind + shadcn/ui</h1>
                    <p className="text-muted-foreground mb-8">
                        Modern React setup with Tailwind CSS and shadcn/ui components
                    </p>
                </div>

                <div className="max-w-md mx-auto space-y-6">
                    <div className="card bg-card border rounded-lg p-6">
                        <h2 className="text-xl font-semibold mb-4">Component Showcase</h2>

                        <div className="space-y-4">
                            <div>
                                <label htmlFor="sample-input" className="block text-sm font-medium mb-2">
                                    Sample Input
                                </label>
                                <Input
                                    id="sample-input"
                                    placeholder="Type something..."
                                    value={inputValue}
                                    onChange={(e) => setInputValue(e.target.value)}
                                />
                                {inputValue && (
                                    <p className="text-sm text-muted-foreground mt-1">
                                        You typed: {inputValue}
                                    </p>
                                )}
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">
                                    Progress Bar ({progress}%)
                                </label>
                                <Progress value={progress} className="mb-2" />
                                <Button onClick={handleProgress} variant="outline" size="sm">
                                    Update Progress
                                </Button>
                            </div>

                            <div className="space-y-2">
                                <h3 className="text-lg font-medium">Button Variants</h3>
                                <div className="flex flex-wrap gap-2">
                                    <Button onClick={() => setCount((count) => count + 1)}>
                                        Count is {count}
                                    </Button>
                                    <Button variant="secondary" onClick={handleToast}>
                                        Show Toast
                                    </Button>
                                    <Button variant="outline">Outline</Button>
                                    <Button variant="destructive">Destructive</Button>
                                </div>
                                <div className="mt-4 space-y-2">
                                    <Button onClick={handleUploadNavigate} className="w-full">
                                        📁 Go to Upload Page
                                    </Button>
                                    <Button
                                        onClick={() => navigate('/images')}
                                        className="w-full"
                                        variant="secondary"
                                    >
                                        🖼️ View Uploaded Images
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="text-center">
                        <p className="text-sm text-muted-foreground">
                            Edit <code className="bg-muted px-1 py-0.5 rounded">src/App.jsx</code> and save to test HMR
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HomePage