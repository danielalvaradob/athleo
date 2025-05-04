from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum

#This file defines the schemas for the equipment feature of the application.
# The schemas are used to validate and serialize/deserialize data for the equipment.
# The EquipmentBase schema defines the common fields for all equipment entries.
# The EquipmentCreate schema is used when creating a new equipment entry.
# The EquipmentOut schema is used when returning an equipment entry from the API.

class EquipmentBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class EquipmentOut(BaseModel):
    id: UUID
    name: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EquipmentCreate(BaseModel):
    name: str
    user_id: UUID

