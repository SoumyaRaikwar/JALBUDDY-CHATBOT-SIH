"""
Voice processing endpoints for jalBuddy AI
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class VoiceResponse(BaseModel):
    transcript: str
    language: str
    confidence: float
    processing_time: float

@router.post("/process", response_model=VoiceResponse)
async def process_voice(
    audio: UploadFile = File(...),
    language: str = "hi"
):
    """Process voice input and return transcript"""
    try:
        logger.info(f"🎤 Processing voice input in {language}")
        
        # Mock response for now - replace with actual Whisper processing
        return VoiceResponse(
            transcript="भूजल स्तर कैसे चेक करें?",
            language=language,
            confidence=0.95,
            processing_time=1.2
        )
        
    except Exception as e:
        logger.error(f"❌ Voice processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages for voice processing"""
    return {
        "languages": [
            {"code": "hi", "name": "Hindi", "native": "हिंदी"},
            {"code": "en", "name": "English", "native": "English"}
        ]
    }
