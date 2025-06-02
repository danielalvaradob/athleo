# app/db/models/equipment.py

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base import Base
from app.db.models.associations import user_equipment
import enum

class EquipmentType(str, enum.Enum):
    home = "home"
    gym = "gym"

class Equipment(Base):
    """Represents a piece of workout equipment 
    (e.g., dumbbells, bench). Equipment can be shared across 
    multiple users and used in various exercises."""
    __tablename__ = "equipment"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(EquipmentType), nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", secondary=user_equipment, back_populates="equipment")
    exercises = relationship("Exercise", back_populates="equipment")