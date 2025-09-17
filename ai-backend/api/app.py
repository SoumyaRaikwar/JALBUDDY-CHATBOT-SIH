"""
Enhanced FastAPI Application
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config.settings import get_settings
from api.routes import chat, health
from services.ai_service_enhanced import EnhancedAIService

logger = logging.getLogger(__name__)
ai_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ai_service

    # Startup
    logger.info("🚀 Starting Enhanced AI Backend...")
    try:
        ai_service = EnhancedAIService()
        await ai_service.initialize()
        app.state.ai_service = ai_service
        logger.info("✅ AI Service ready with real LLM integration!")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

    yield

    # Shutdown
    if ai_service:
        await ai_service.cleanup()

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.get("/")
    async def root():
        return {
            "message": "jalBuddy AI Enhanced - Competition Ready!",
            "version": settings.VERSION,
            "features": [
                "Real GPT-4 Integration",
                "Multi-LLM Architecture", 
                "Advanced RAG System",
                "Voice Processing Ready",
                "INGRES Integration",
                "Hindi/English Support"
            ],
            "endpoints": {
                "docs": "/docs",
                "health": "/api/health", 
                "chat": "/api/chat/query"
            }
        }

    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

    return app
