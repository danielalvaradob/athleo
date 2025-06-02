# app/db/models/user.py

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from datetime import datetime, timezone

from app.db.base import Base
from app.db.models.associations import user_trainers, user_equipment
import enum

class UserRole(str, enum.Enum):
    user = "user"
    trainer = "trainer"
    admin = "admin"

class UserLanguage(str, enum.Enum):
    en = "en"
    es = "es"

class User(Base):
    """Represents an account in the system.
    A user can be a regular trainee, a trainer, or an admin.
    Users can have routines, exercise logs, and are optionally
    linked to trainers via many-to-many relationships."""
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    language = Column(SQLEnum(UserLanguage), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Trainer-trainee many-to-many relationships
    trainers = relationship(
        "User",
        secondary=user_trainers,
        primaryjoin=id == user_trainers.c.trainee_id,
        secondaryjoin=id == user_trainers.c.trainer_id,
        back_populates="trainees"
    )

    trainees = relationship(
        "User",
        secondary=user_trainers,
        primaryjoin=id == user_trainers.c.trainer_id,
        secondaryjoin=id == user_trainers.c.trainee_id,
        back_populates="trainers"
    )
    
    # Equipment relationship
    equipment = relationship("Equipment", secondary=user_equipment, back_populates="users")

    # Exercise logs relationship
    exercise_logs = relationship("ExerciseLog", back_populates="user")

    # Add the missing routines relationship
    routines = relationship("Routine", back_populates="user")