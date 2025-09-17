"""
Database initialization for jalBuddy AI Backend
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import get_settings

logger = logging.getLogger(__name__)

Base = declarative_base()
engine = None
SessionLocal = None

async def init_db():
    """Initialize database connection"""
    global engine, SessionLocal
    
    try:
        settings = get_settings()
        logger.info(f"🗄️ Initializing database: {settings.DATABASE_URL}")
        
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
