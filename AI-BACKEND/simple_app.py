"""
Simple JalBuddy FastAPI Application
Basic chatbot functionality without complex dependencies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uvicorn
from datetime import datetime

from services.simple_chatbot import SimpleChatbot
from config.settings import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings and chatbot
settings = get_settings()
chatbot = SimpleChatbot()

# Create FastAPI app
app = FastAPI(
    title="JalBuddy AI Backend - Simple",
    description="Basic groundwater consultation chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = None
    user_id: Optional[str] = "default"
    location: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    language: str
    confidence: float
    response_type: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

# Routes
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "🌊 Welcome to JalBuddy API!",
        "description": "AI-powered groundwater consultation system",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services={
            "chatbot": "operational",
            "api": "operational"
        }
    )

@app.post("/api/chat/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Process a chat query"""
    try:
        logger.info(f"🗨️ Chat query: {request.query[:50]}...")
        
        # Prepare context
        context = {}
        if request.location:
            context["location"] = request.location
        
        # Process message with chatbot
        result = chatbot.process_message(
            message=request.query,
            user_id=request.user_id,
            context=context if context else None
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Chat query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/examples")
async def get_examples():
    """Get example queries for testing"""
    return {
        "english_examples": [
            "Hello, I need help with groundwater",
            "What are the borewell construction guidelines?",
            "How do I check water quality?",
            "Tell me about GEC classification",
            "What are groundwater recharge methods?",
            "Is my water safe to drink?",
            "How deep can I drill a borewell?"
        ],
        "hindi_examples": [
            "नमस्ते, मुझे भूजल के बारे में जानकारी चाहिए",
            "बोरवेल बनाने के नियम क्या हैं?",
            "पानी की गुणवत्ता कैसे जांचें?",
            "GEC वर्गीकरण के बारे में बताएं",
            "भूजल रिचार्ज के तरीके क्या हैं?",
            "क्या मेरा पानी पीने योग्य है?",
            "बोरवेल कितनी गहरी खुदाई कर सकते हैं?"
        ]
    }

@app.get("/api/chat/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 10):
    """Get chat history for a user"""
    try:
        history = chatbot.get_conversation_history(user_id=user_id, limit=limit)
        return {"user_id": user_id, "history": history, "count": len(history)}
    except Exception as e:
        logger.error(f"❌ History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/chat/history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history for a user"""
    try:
        chatbot.clear_history(user_id=user_id)
        return {"message": f"Chat history cleared for user {user_id}"}
    except Exception as e:
        logger.error(f"❌ History clearing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/stats")
async def get_chat_stats():
    """Get chatbot statistics"""
    total_conversations = len(chatbot.conversation_history)
    unique_users = len(set(conv['user_id'] for conv in chatbot.conversation_history))
    
    # Language distribution
    languages = {}
    for conv in chatbot.conversation_history:
        lang = conv.get('language', 'unknown')
        languages[lang] = languages.get(lang, 0) + 1
    
    return {
        "total_conversations": total_conversations,
        "unique_users": unique_users,
        "language_distribution": languages,
        "uptime": datetime.now().isoformat()
    }

# Mock INGRES endpoints for testing
@app.get("/api/ingres/data/{location}")
async def get_ingres_data(location: str):
    """Mock INGRES data endpoint"""
    # This would normally fetch real data from INGRES API
    mock_data = {
        "location": location,
        "groundwater_level": {
            "data": {
                "water_level_mbgl": 15.5,
                "status": "declining",
                "gec_category": "Semi-Critical",
                "last_updated": "2025-01-15"
            }
        },
        "water_quality": {
            "data": {
                "parameters": {
                    "tds": 650,
                    "fluoride": 1.2,
                    "nitrate": 35,
                    "ph": 7.8,
                    "chloride": 180
                },
                "assessment": "Acceptable for drinking with treatment",
                "last_tested": "2025-01-10"
            }
        }
    }
    
    logger.info(f"📊 Mock INGRES data requested for: {location}")
    return mock_data

@app.get("/api/ingres/locations")
async def get_ingres_locations():
    """Mock INGRES locations endpoint"""
    return {
        "locations": [
            "Hyderabad",
            "Bangalore", 
            "Chennai",
            "Mumbai",
            "Delhi",
            "Pune",
            "Kolkata",
            "Ahmedabad",
            "Jaipur",
            "Lucknow"
        ]
    }

if __name__ == "__main__":
    logger.info("🚀 Starting JalBuddy Simple Backend...")
    uvicorn.run(
        "simple_app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )