from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional
from fastapi import HTTPException

class UserRole(str, Enum):
    user = "user"
    trainer = "trainer"
    admin = "admin"

class UserLanguage(str, Enum):
    en = "en"
    es = "es"

class UserBase(BaseModel):
    email: Optional[EmailStr] = None  # Optional for AI trainers
    name: str
    role: UserRole
    language: UserLanguage
    is_ai_trainer: bool = False  # Indicates if the user is an AI trainer

class UserCreate(UserBase):
    password: Optional[str] = None  # Optional for AI trainers

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
