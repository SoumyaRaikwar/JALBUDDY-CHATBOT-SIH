"""
Chat endpoints for jalBuddy AI
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from services.ai_service import AIService

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatQuery(BaseModel):
    query: str
    language: str = "hi"
    user_id: Optional[str] = "anonymous"
    location: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float
    sources: list
    language: str
    processing_time: float
    timestamp: str

def get_ai_service(request: Request) -> AIService:
    """Dependency to get AI service from app state"""
    ai_service = getattr(request.app.state, 'ai_service', None)
    if not ai_service:
        raise HTTPException(status_code=503, detail="AI service not initialized")
    return ai_service

@router.post("/query", response_model=ChatResponse)
async def process_chat_query(
    query: ChatQuery,
    ai_service: AIService = Depends(get_ai_service)
):
    """Process a text-based groundwater query"""
    try:
        logger.info(f"💬 Chat query from {query.user_id}: {query.query[:50]}...")

        user_context = {
            "user_id": query.user_id,
            "location": query.location,
            **(query.context or {})
        }

        result = await ai_service.process_query(
            query=query.query,
            language=query.language,
            user_context=user_context
        )

        return ChatResponse(
            response=result["response"],
            confidence=result["confidence"],
            sources=result["sources"],
            language=result["language"],
            processing_time=result["processing_time"],
            timestamp=result["timestamp"]
        )

    except Exception as e:
        logger.error(f"❌ Chat query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/examples")
async def get_example_queries():
    """Get example queries for different scenarios"""
    examples = {
        "hindi": [
            "भूजल स्तर कैसे चेक करें?",
            "बोरवेल ड्रिलिंग के लिए सही जगह कैसे चुनें?",
            "भूजल रिचार्ज कैसे बढ़ाएं?",
            "हार्ड रॉक एरिया में पानी कैसे खोजें?",
            "GEC-2015 गाइडलाइन क्या है?"
        ],
        "english": [
            "How to check groundwater level?",
            "What is GEC-2015 methodology?",
            "How to select location for borewell drilling?",
            "Methods for groundwater recharge enhancement",
            "Characteristics of hard rock aquifers"
        ]
    }

    return {
        "examples": examples,
        "message": "Use these example queries to test jalBuddy's capabilities"
    }
