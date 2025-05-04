from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

# This file defines the schemas for a single day in a training routine.
# Each RoutineDay groups exercises under a specific name (e.g., "Legs", "Push").
# It belongs to a specific routine and has a defined order in the week (1–7).

class RoutineDayBase(BaseModel):
    day_number: int = Field(ge=1, le=7)  # Day of the week: 1 = Monday, 7 = Sunday
    name: str                            # Custom label: "Legs", "Full Body", etc.

class RoutineDayCreate(RoutineDayBase):
    routine_id: UUID

class RoutineDayOut(RoutineDayBase):
    id: UUID
    routine_id: UUID
    model_config = ConfigDict(from_attributes=True)