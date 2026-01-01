"""
Database connection management for the connector API.
"""
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

from sqlmodel import SQLModel

from .config import settings

# Convert sync URL to async URL for asyncmy
async_database_url = settings.database_url.replace("mysql://", "mysql+asyncmy://")

# Async SQLAlchemy setup
async_engine = create_async_engine(
    async_database_url,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    echo=settings.debug,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_database():
    """Create all database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    """Drop all database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def test_connection() -> bool:
    """Test async database connection."""
    try:
        async with async_engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False


async def get_database_info() -> dict:
    """Get database connection information."""
    return {
        "database_url": async_database_url.replace(settings.database_password or "", "***"),
        "pool_size": async_engine.pool.size(),
        "checked_out": async_engine.pool.checkedout(),
        "invalid": async_engine.pool.invalid(),
        "overflow": async_engine.pool.overflow(),
    }


# Legacy sync functions for backward compatibility
def get_db():
    """Get database session (deprecated - use get_async_db)."""
    raise DeprecationWarning("Use get_async_db() for async operations")


def create_database_sync():
    """Create all database tables (deprecated - use create_database)."""
    raise DeprecationWarning("Use create_database() for async operations")


def drop_database_sync():
    """Drop all database tables (deprecated - use drop_database)."""
    raise DeprecationWarning("Use drop_database() for async operations")


def test_connection_sync() -> bool:
    """Test database connection (deprecated - use test_connection)."""
    raise DeprecationWarning("Use test_connection() for async operations")


def get_database_info_sync() -> dict:
    """Get database connection information (deprecated - use get_database_info)."""
    raise DeprecationWarning("Use get_database_info() for async operations")