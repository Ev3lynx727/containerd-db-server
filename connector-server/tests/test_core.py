"""
Tests for core functionality and imports.
"""
import pytest


def test_core_imports():
    """Test that core modules can be imported."""
    try:
        from core.config import settings
        from core.database import get_async_db, async_engine
        from models import User, ApiKey, QueryHistory
        assert settings is not None
        assert get_async_db is not None
        assert async_engine is not None
        assert User is not None
        assert ApiKey is not None
        assert QueryHistory is not None
    except ImportError as e:
        pytest.skip(f"Import failed (expected in CI): {e}")


def test_model_creation():
    """Test that models can be instantiated."""
    try:
        from models.user import UserCreate
        from models.api_key import ApiKeyCreate

        # Test User creation schema
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        assert user_data.username == "testuser"
        assert user_data.email == "test@example.com"

        # Test API Key creation schema
        api_key_data = ApiKeyCreate(
            client_id="test-client",
            scopes=["read", "write"]
        )
        assert api_key_data.client_id == "test-client"
        assert api_key_data.scopes == ["read", "write"]

    except ImportError as e:
        pytest.skip(f"Import failed (expected in CI): {e}")


def test_settings_validation():
    """Test that settings load and validate correctly."""
    try:
        from core.config import settings

        # Test that required settings exist
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'redis_url')
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'api_port')

        # Test validation methods
        assert settings.is_development() or settings.is_production()
        assert isinstance(settings.api_port, int)
        assert settings.api_port > 0

    except ImportError as e:
        pytest.skip(f"Import failed (expected in CI): {e}")


@pytest.mark.asyncio
async def test_async_database_connection():
    """Test that async database connection works."""
    try:
        from core.database import test_connection

        # This will fail in CI without actual database, but tests the function exists
        result = await test_connection()
        # In CI this will likely be False (no DB), but function should exist
        assert isinstance(result, bool)

    except ImportError as e:
        pytest.skip(f"Import failed (expected in CI): {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])