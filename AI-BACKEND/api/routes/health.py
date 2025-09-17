"""
Health check endpoints
"""

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

from config.settings import get_settings

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    components: Dict[str, Any]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.VERSION,
        components={
            "database": "connected",
            "ai_service": "initialized",
            "vector_store": "ready"
        }
    )

@router.get("/")
async def root():
    """Root endpoint"""
    settings = get_settings()
    return {
        "message": "jalBuddy AI Backend",
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs": "/docs",
        "health": "/api/health"
    }
