from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import date
from typing import Optional

# This file defines the schemas for the exercise log feature of the application.
# The schemas are used to validate and serialize/deserialize data for the exercise log.

class ExerciseLogBase(BaseModel):
    weight: float = Field(ge=0)
    reps: int = Field(ge=0)
    sets: int = Field(ge=0)
    date: date
    notes: Optional[str] = None  # Optional field, used by AI for summaries or context

class ExerciseLogCreate(ExerciseLogBase):
    user_id: UUID
    exercise_id: UUID

class ExerciseLogOut(ExerciseLogBase):
    id: UUID
    user_id: UUID
    exercise_id: UUID
    model_config = ConfigDict(from_attributes=True)