"""
User model for the database connector.
"""
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .query_history import QueryHistory


class User(SQLModel, table=True):
    """User model with SQLModel."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=50, unique=True, index=True, nullable=False)
    email: Optional[str] = Field(max_length=100, unique=True, index=True)
    hashed_password: str = Field(max_length=128, nullable=False)
    is_active: bool = Field(default=True)
    scopes: str = Field(default="", max_length=500)  # Comma-separated scopes

    # Relationships
    query_history: List["QueryHistory"] = Relationship(back_populates="user")

    @property
    def scopes_list(self) -> List[str]:
        """Get scopes as a list."""
        return self.scopes.split(",") if self.scopes else []

    @scopes_list.setter
    def scopes_list(self, value: List[str]):
        """Set scopes from a list."""
        self.scopes = ",".join(value)

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        arbitrary_types_allowed = True


class UserCreate(SQLModel):
    """User creation schema."""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    scopes: Optional[List[str]] = Field(default_factory=list)


class UserRead(SQLModel):
    """User read schema."""
    id: int
    username: str
    email: Optional[str]
    is_active: bool
    scopes: List[str]


class UserUpdate(SQLModel):
    """User update schema."""
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = Field(default=None, min_length=5, max_length=100)
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    is_active: Optional[bool] = None
    scopes: Optional[List[str]] = None
