"""
jalBuddy Configuration Settings
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application Info
    PROJECT_NAME: str = "jalBuddy AI Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered Groundwater Consultation System for SIH 2025"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./jalbuddy.db"

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"

    # Vector Database Settings
    VECTOR_STORE_TYPE: str = "chromadb"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # RAG Configuration
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7

    # AI Model Configuration
    LLAMA_MODEL: str = "microsoft/DialoGPT-medium"
    GPT4ALL_MODEL_PATH: str = "./models/gpt4all-model.gguf"

    # Whisper Configuration
    WHISPER_MODEL: str = "base"
    SUPPORTED_LANGUAGES: List[str] = ["hi", "en"]

    # INGRES API Configuration
    INGRES_BASE_URL: str = "https://ingres.iith.ac.in/api"
    INGRES_API_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "jalbuddy-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Paths
    DATA_DIR: str = "./data"
    MODELS_DIR: str = "./models"
    DOCUMENTS_DIR: str = "./data/documents"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

# Create directories on import
settings = get_settings()
for directory in [settings.DATA_DIR, settings.MODELS_DIR, settings.DOCUMENTS_DIR]:
    os.makedirs(directory, exist_ok=True)
