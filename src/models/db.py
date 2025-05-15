from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.settings.config import settings
import logging

logger = logging.getLogger(__name__)

"""
Database connection and session management.
"""

try:
    # Create a new SQLAlchemy engine instance
    engine = create_engine(settings.database_url, echo=True, future=True)
    # Create a configured "Session" class
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base = declarative_base()
    logger.info("Database engine and session initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise