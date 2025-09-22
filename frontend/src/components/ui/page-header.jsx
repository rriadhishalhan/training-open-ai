import { Button } from './button'
import { useNavigate } from 'react-router-dom'

export function PageHeader({ title }) {
    const navigate = useNavigate()

    return (
        <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">{title}</h1>
            <Button
                variant="outline"
                size="sm"
                onClick={() => navigate('/')}
            >
                🏠 Back to Home
            </Button>
        </div>
    )
}