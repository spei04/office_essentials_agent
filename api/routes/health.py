"""
Health check routes.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "office-essentials-agent-api",
    }

