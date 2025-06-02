# app/db/models/associations.py

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.db.base import Base
from app.db.base import Base

"""Association table linking users with the equipment they have access to.
Used for customizing AI-generated workouts."""
user_equipment = Table(
    "user_equipment",
    Base.metadata,  # Use Base.metadata to ensure it's part of the same metadata
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("equipment_id", ForeignKey("equipment.id"), primary_key=True),
    extend_existing=True,  # Allow redefinition of the table
)

"""Association table linking exercises with specific days
in a workout routine."""
routine_day_exercises = Table(
    "routine_day_exercises",
    Base.metadata,
    Column("routine_day_id", ForeignKey("routine_days.id"), primary_key=True),
    Column("exercise_id", ForeignKey("exercises.id"), primary_key=True),
    extend_existing=True,  # Allow redefinition of the table
)

"""Association table to model the many-to-many relationship
between users and their trainers."""
user_trainers = Table(
    "user_trainers",
    Base.metadata,
    Column("trainee_id", PGUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("trainer_id", PGUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)