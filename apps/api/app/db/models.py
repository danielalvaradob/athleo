from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum, DateTime, Table, Integer, Float, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4
from app.db.session import Base
import enum


# Enum definition for user roles
class UserRole(str, enum.Enum):
    user = "user"
    trainer = "trainer"
    admin = "admin"

# Enum definition for supported UI languages
class UserLanguage(str, enum.Enum):
    en = "en"
    es = "es"

# Association table for Many-to-Many relationship
metadata = MetaData()

user_equipment = Table(
    "user_equipment",
    metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("equipment_id", ForeignKey("equipment.id"), primary_key=True),
    extend_existing=True,  # Allow redefinition of the table
)

routine_day_exercises = Table(
    "routine_day_exercises",
    metadata,
    Column("routine_day_id", ForeignKey("routine_days.id"), primary_key=True),
    Column("exercise_id", ForeignKey("exercises.id"), primary_key=True),
    extend_existing=True,  # Allow redefinition of the table
)

user_trainers = Table(
    "user_trainers",
    Base.metadata,
    Column("trainee_id", PGUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("trainer_id", PGUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)

# SQLAlchemy model representing a user in the system.
# This model stores authentication data and profile information.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Use string references for relationships
    trainers = relationship("User", secondary="user_trainers", primaryjoin="User.id == user_trainers.c.trainee_id")

# Enum for equipment type
class EquipmentType(str, enum.Enum):
    home = "home"
    gym = "gym"



class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(EquipmentType), nullable=False)  # Type: home or gym

    created_at = Column(
        DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc))

    # Relationships
    users = relationship("User", secondary=user_equipment, back_populates="equipment")
    exercises = relationship("Exercise", back_populates="equipment")

class Exercise(Base):
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

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(PGUUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False, index=True)

    weight = Column(Float, nullable=False)  # Weight used for the exercise
    reps = Column(Integer, nullable=False)  # Number of reps performed
    sets = Column(Integer, nullable=False)  # Number of sets performed
    date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    notes = Column(String, nullable=True)  # Optional notes for the log

    # Relationships
    user = relationship("User", back_populates="exercise_logs")
    exercise = relationship("Exercise", back_populates="exercise_logs")

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

class Routine(Base):
    __tablename__ = "routines"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="routines")
    routine_days = relationship("RoutineDay", back_populates="routine", cascade="all, delete-orphan")

class RoutineDay(Base):
    __tablename__ = "routine_days"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    day_number = Column(Integer, nullable=False)  # 1 = Monday, 7 = Sunday
    name = Column(String, nullable=False)  # Custom label: "Legs", "Push", etc.
    routine_id = Column(PGUUID(as_uuid=True), ForeignKey("routines.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    routine = relationship("Routine", back_populates="routine_days")
    exercises = relationship("Exercise", secondary=routine_day_exercises, back_populates="routine_days")


