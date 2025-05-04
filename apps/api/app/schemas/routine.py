from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List
from app.schemas.routine_day import RoutineDayOut

# This file defines the schemas for training routines.
# A routine groups routine days and belongs to a single user.

class RoutineBase(BaseModel):
    name: str
    is_active: bool = False

class RoutineCreate(RoutineBase):
    user_id: UUID

class RoutineOut(RoutineBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    routine_days: List[RoutineDayOut] = []
    model_config = ConfigDict(from_attributes=True)