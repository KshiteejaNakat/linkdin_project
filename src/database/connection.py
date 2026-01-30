"""
Database Connection Module
Handles database connection and session management.
"""

from typing import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

from .models import Base

# Default database URL (SQLite for development)
DATABASE_URL = "sqlite:///./career_architect.db"

engine = None
SessionLocal = None


def init_db(database_url: str = DATABASE_URL) -> None:
    """
    Initialize database connection and create tables.
    
    Args:
        database_url: Database connection URL
    """
    global engine, SessionLocal
    
    logger.info(f"Initializing database: {database_url}")
    
    # Create engine
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
        echo=False
    )
    
    # Create session factory
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database initialized successfully")


def get_db() -> Generator[Session, None, None]:
    """
    Get database session generator.
    
    Yields:
        Database session
    """
    if SessionLocal is None:
        init_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Usage:
        with get_db_session() as db:
            db.query(User).all()
    """
    if SessionLocal is None:
        init_db()
    
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()


def reset_database() -> None:
    """Reset database (drop and recreate all tables)."""
    global engine
    
    if engine is None:
        init_db()
    
    logger.warning("Resetting database - all data will be lost!")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database reset complete")
