"""
Database models for the connector server.
"""
from .user import User, UserCreate, UserRead, UserUpdate
from .api_key import ApiKey, ApiKeyCreate, ApiKeyRead, ApiKeyUpdate
from .query_history import (
    QueryHistory,
    QueryHistoryCreate,
    QueryHistoryRead,
    QueryHistoryUpdate,
    QueryStatus,
)

__all__ = [
    # User models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # API Key models
    "ApiKey",
    "ApiKeyCreate",
    "ApiKeyRead",
    "ApiKeyUpdate",
    # Query History models
    "QueryHistory",
    "QueryHistoryCreate",
    "QueryHistoryRead",
    "QueryHistoryUpdate",
    "QueryStatus",
]
