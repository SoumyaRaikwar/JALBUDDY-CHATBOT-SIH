#!/usr/bin/env python3
"""
jalBuddy AI Enhanced Backend - Main Entry Point
Smart India Hackathon 2025 - Competition Ready
"""

import uvicorn
import logging
from api.app import create_app
from config.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    settings = get_settings()
    logger.info("🚀 Starting jalBuddy AI Enhanced")

    app = create_app()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)

if __name__ == "__main__":
    main()
