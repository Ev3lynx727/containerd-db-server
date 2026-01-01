"""
Query History model for the database connector.
"""
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, Enum
from sqlalchemy.sql import func

from ..core.database import Base


class QueryHistory(Base):
    """Query History model."""
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True)
    connection_id = Column(String(100))
    query = Column(Text, nullable=False)
    execution_time = Column(Float)
    row_count = Column(Integer, default=0)
    status = Column(Enum('success', 'error', name='query_status'), default='success')
    error_message = Column(Text)
    executed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    user = relationship("User", back_populates="query_history")