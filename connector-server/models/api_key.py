"""
API Key model for the database connector.
"""
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from ..core.database import Base


class ApiKey(Base):
    """API Key model."""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_id = Column(String(16), unique=True, nullable=False, index=True)
    key_hash = Column(String(128), unique=True, nullable=False, index=True)
    client_id = Column(String(100), nullable=False, index=True)
    scopes = Column(Text, default="[]")  # JSON array of scopes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=1000)
    last_used = Column(DateTime(timezone=True), nullable=True)

    @property
    def scopes_list(self) -> List[str]:
        """Get scopes as a list."""
        import json
        try:
            return json.loads(self.scopes) if self.scopes else []
        except json.JSONDecodeError:
            return []

    @scopes_list.setter
    def scopes_list(self, value: List[str]):
        """Set scopes from a list."""
        import json
        self.scopes = json.dumps(value)

    def is_expired(self) -> bool:
        """Check if the API key is expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at.replace(tzinfo=None)