"""
Query History model for the database connector.
"""
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class QueryStatus(str, PyEnum):
    """Query execution status."""
    SUCCESS = "success"
    ERROR = "error"


class QueryHistory(SQLModel, table=True):
    """Query History model with SQLModel."""
    __tablename__ = "query_history"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[str] = Field(
        max_length=100, index=True, foreign_key="users.username"
    )
    connection_id: Optional[str] = Field(max_length=100)
    query: str = Field(nullable=False)
    execution_time: Optional[float] = None
    row_count: int = Field(default=0)
    status: QueryStatus = Field(default=QueryStatus.SUCCESS)
    error_message: Optional[str] = None
    executed_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship
    user: Optional["User"] = Relationship(back_populates="query_history")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        arbitrary_types_allowed = True


class QueryHistoryCreate(SQLModel):
    """Query History creation schema."""
    user_id: Optional[str] = Field(default=None, max_length=100)
    connection_id: Optional[str] = Field(default=None, max_length=100)
    query: str = Field(min_length=1)
    execution_time: Optional[float] = Field(default=None, ge=0)
    row_count: int = Field(default=0, ge=0)
    status: QueryStatus = Field(default=QueryStatus.SUCCESS)
    error_message: Optional[str] = None


class QueryHistoryRead(SQLModel):
    """Query History read schema."""
    id: int
    user_id: Optional[str]
    connection_id: Optional[str]
    query: str
    execution_time: Optional[float]
    row_count: int
    status: QueryStatus
    error_message: Optional[str]
    executed_at: datetime


class QueryHistoryUpdate(SQLModel):
    """Query History update schema."""
    user_id: Optional[str] = Field(default=None, max_length=100)
    connection_id: Optional[str] = Field(default=None, max_length=100)
    query: Optional[str] = Field(default=None, min_length=1)
    execution_time: Optional[float] = Field(default=None, ge=0)
    row_count: Optional[int] = Field(default=None, ge=0)
    status: Optional[QueryStatus] = None
    error_message: Optional[str] = None
