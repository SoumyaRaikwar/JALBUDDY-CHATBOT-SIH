#!/usr/bin/env python3
"""
jalBuddy AI Backend - Main Application Entry Point
Smart India Hackathon 2025
"""

import uvicorn
from config.settings import get_settings

def main():
    settings = get_settings()

    uvicorn.run(
        "api.app:create_app",
        factory=True,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()
