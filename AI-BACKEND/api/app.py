"""
FastAPI Application Factory for jalBuddy AI Backend
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from contextlib import asynccontextmanager

from config.settings import get_settings
from api.routes import chat, voice, health, ingres
from core.database import init_db
from services.ai_service import AIService
from services.ingres_service import IngresService
from services.rag_service_chroma import ChromaRAGService

logger = logging.getLogger(__name__)

ai_service = None
ingres_service = None
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    global ai_service, ingres_service, rag_service

    logger.info("🚀 Starting jalBuddy AI Backend...")

    try:
        await init_db()
        logger.info("✅ Database initialized")

        # Initialize INGRES service
        ingres_service = IngresService()
        await ingres_service.initialize()
        app.state.ingres_service = ingres_service
        logger.info("✅ INGRES service initialized")

        # Initialize RAG service
        rag_service = ChromaRAGService()
        await rag_service.initialize()
        app.state.rag_service = rag_service
        logger.info("✅ RAG service initialized")

        # Initialize AI service with dependencies
        ai_service = AIService(
            rag_service=rag_service,
            ingres_service=ingres_service
        )
        await ai_service.initialize()
        app.state.ai_service = ai_service
        logger.info("✅ AI service initialized")

        logger.info("🎯 jalBuddy backend is ready!")

    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise

    yield

    logger.info("🛑 Shutting down jalBuddy AI Backend...")
    if rag_service:
        await rag_service.cleanup()
    if ingres_service:
        await ingres_service.cleanup()
    if ai_service:
        await ai_service.cleanup()
    logger.info("👋 Shutdown complete")

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        logger.info(f"📥 {request.method} {request.url}")
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"📤 {response.status_code} - {process_time:.3f}s")
        return response

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"🚨 Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "कुछ तकनीकी समस्या हुई है। कृपया बाद में कोशिश करें।"
            }
        )

    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(voice.router, prefix="/api/voice", tags=["voice"])
    app.include_router(ingres.router, prefix="/api/ingres", tags=["ingres"])

    return app
