"""
User model for the database connector.
"""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    scopes = Column(String(500), default="")  # Comma-separated scopes

    # Relationships
    query_history = relationship("QueryHistory", back_populates="user")

    @property
    def scopes_list(self) -> list[str]:
        """Get scopes as a list."""
        return self.scopes.split(",") if self.scopes else []

    @scopes_list.setter
    def scopes_list(self, value: list[str]):
        """Set scopes from a list."""
        self.scopes = ",".join(value)