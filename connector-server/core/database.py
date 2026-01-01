"""
Database connection management for the connector API.
"""
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from .config import settings

# SQLAlchemy setup
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def drop_database():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


def test_connection() -> bool:
    """Test database connection."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def get_database_info() -> dict:
    """Get database connection information."""
    return {
        "database_url": settings.database_url.replace(settings.database_password or "", "***"),
        "pool_size": engine.pool.size(),
        "checked_out": engine.pool.checkedout(),
        "invalid": engine.pool.invalid(),
        "overflow": engine.pool.overflow(),
    }