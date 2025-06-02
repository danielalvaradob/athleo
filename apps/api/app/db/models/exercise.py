from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, DateTime, Table, Integer, Float, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from app.db.base import Base
from app.db.models.associations import routine_day_exercises
import enum

class Exercise(Base):
    """Defines an individual exercise, including reps,
    sets, suggested weight, and rest time.
    Each exercise can optionally be associated with equipment 
    and is reused across multiple routine days."""
    __tablename__ = "exercises"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_suggestion = Column(Float, nullable=True)  # Optional weight suggestion
    rest_seconds = Column(Integer, nullable=False, default=60)  # Rest time between sets
    video_url = Column(String, nullable=True)  # Optional video link for guidance
    notes = Column(String, nullable=True)  # Optional notes for the exercise

    # Relationships
    equipment_id = Column(PGUUID(as_uuid=True), ForeignKey("equipment.id"), nullable=True)
    equipment = relationship("Equipment", back_populates="exercises")  # Equipment used for this exercise
    exercise_logs = relationship("ExerciseLog", back_populates="exercise")
    routine_days = relationship("RoutineDay", secondary=routine_day_exercises, back_populates="exercises")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )