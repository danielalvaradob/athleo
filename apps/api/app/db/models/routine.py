from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, DateTime, Table, Integer, Float, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from uuid import uuid4
from app.db.base import Base
import enum

class Routine(Base):
    """Represents a full workout plan assigned to a user. 
    A routine is composed of multiple routine days 
    (e.g., Push, Legs, Pull)."""
    __tablename__ = "routines"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user = relationship("User", back_populates="routines")
    routine_days = relationship("RoutineDay", back_populates="routine", cascade="all, delete-orphan")
