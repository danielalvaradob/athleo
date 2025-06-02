from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, DateTime, Table, Integer, Float, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
from uuid import uuid4
from app.db.base import Base
from app.db.models.associations import routine_day_exercises
import enum

class RoutineDay(Base):
    """Represents a day within a routine (e.g., 'Monday - Push Day').
    Contains a list of exercises to perform on that day."""
    __tablename__ = "routine_days"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    day_number = Column(Integer, nullable=False)  # 1 = Monday, 7 = Sunday
    name = Column(String, nullable=False)  # Custom label: "Legs", "Push", etc.
    routine_id = Column(PGUUID(as_uuid=True), ForeignKey("routines.id"), nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    routine = relationship("Routine", back_populates="routine_days")
    exercises = relationship("Exercise", secondary=routine_day_exercises, back_populates="routine_days")
