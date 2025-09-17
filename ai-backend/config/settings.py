"""
jalBuddy Enhanced Configuration
"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App Info
    PROJECT_NAME: str = "jalBuddy AI Enhanced"
    VERSION: str = "2.0.0"
    DESCRIPTION: str = "Competition-Ready AI Groundwater System"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # AI Models
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Government/External APIs
    INGRES_API: str = "https://ingres.iith.ac.in/api/v1"
    WRIS_API: str = "https://indiawris.gov.in/api/v1"
    CGWB_API: str = "https://cgwb.gov.in/api/v1"
    BHASHINI_API: str = "https://bhashini.gov.in/ulca/apis/v0"
    WHATSAPP_API: str = "https://graph.facebook.com/v18.0"

    # Database
    DATABASE_URL: str = "sqlite:///./jalbuddy.db"

    # Features
    ENABLE_VOICE_PROCESSING: bool = True
    ENABLE_OFFLINE_MODE: bool = True

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
