from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, DateTime, Table, Integer, Float, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from app.db.base import Base
import enum

class ExerciseLog(Base):
    """Logs a user’s performance for a specific exercise on a
    specific day. Includes reps, weight, and notes used 
    for AI insights."""
    __tablename__ = "exercise_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(PGUUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False, index=True)

    weight = Column(Float, nullable=False)  # Weight used for the exercise
    reps = Column(Integer, nullable=False)  # Number of reps performed
    sets = Column(Integer, nullable=False)  # Number of sets performed
    date = Column(DateTime, nullable=False, default=func.now())
    notes = Column(String, nullable=True)  # Optional notes for the log

    # Relationships
    user = relationship("User", back_populates="exercise_logs")
    exercise = relationship("Exercise", back_populates="exercise_logs")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )