"""
Health Check Routes
"""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Enhanced health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="2.0.0"
    )

@router.get("/stats")
async def get_stats(request: Request):
    """Get system statistics"""
    ai_service = getattr(request.app.state, 'ai_service', None)
    if ai_service:
        return await ai_service.get_stats()
    return {"status": "service_not_ready"}
