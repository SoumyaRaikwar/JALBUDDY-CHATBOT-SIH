"""
Enhanced Chat Routes
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatQuery(BaseModel):
    query: str
    language: str = "hi"
    user_id: Optional[str] = "anonymous"
    location: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float
    model_used: str
    processing_time: float
    timestamp: str
    response_type: str = "text"

def get_ai_service(request: Request):
    """Get AI service from app state"""
    ai_service = getattr(request.app.state, 'ai_service', None)
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not ready")
    return ai_service

@router.post("/query", response_model=ChatResponse)
async def process_chat_query(query: ChatQuery, ai_service = Depends(get_ai_service)):
    """Process enhanced chat query with real AI"""
    try:
        logger.info(f"💬 Enhanced query: {query.query[:50]}...")

        user_context = {
            "user_id": query.user_id,
            "location": query.location
        }

        result = await ai_service.process_query(
            query=query.query,
            language=query.language,
            user_context=user_context
        )

        return ChatResponse(
            response=result["response"],
            confidence=result["confidence"], 
            model_used=result["model_used"],
            processing_time=result["processing_time"],
            timestamp=result["timestamp"],
            response_type=result.get("response_type", "text")
        )

    except Exception as e:
        logger.error(f"❌ Chat query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/examples")
async def get_examples():
    """Get example queries"""
    return {
        "hindi_examples": [
            "भूजल स्तर कैसे चेक करें?",
            "बोरवेल ड्रिलिंग के लिए सही जगह कैसे चुनें?",
            "भूजल रिचार्ज कैसे बढ़ाएं?"
        ],
        "english_examples": [
            "How to check groundwater level?",
            "Best location for borewell drilling?", 
            "Methods for groundwater recharge?"
        ]
    }
