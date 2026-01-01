"""
API Key model for the database connector.
"""
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel


class ApiKey(SQLModel, table=True):
    """API Key model with SQLModel."""
    __tablename__ = "api_keys"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    key_id: str = Field(max_length=16, unique=True, nullable=False, index=True)
    key_hash: str = Field(max_length=128, unique=True, nullable=False, index=True)
    client_id: str = Field(max_length=100, nullable=False, index=True)
    scopes: str = Field(default="[]", max_length=1000)  # JSON array of scopes
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = Field(default=True)
    rate_limit: int = Field(default=1000)
    last_used: Optional[datetime] = None

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
        return datetime.utcnow() > self.expires_at

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        arbitrary_types_allowed = True


class ApiKeyCreate(SQLModel):
    """API Key creation schema."""
    client_id: str = Field(min_length=1, max_length=100)
    scopes: List[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None
    rate_limit: int = Field(default=1000, ge=1, le=10000)


class ApiKeyRead(SQLModel):
    """API Key read schema."""
    id: int
    key_id: str
    client_id: str
    scopes: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    rate_limit: int
    last_used: Optional[datetime]


class ApiKeyUpdate(SQLModel):
    """API Key update schema."""
    client_id: Optional[str] = Field(default=None, min_length=1, max_length=100)
    scopes: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    rate_limit: Optional[int] = Field(default=None, ge=1, le=10000)