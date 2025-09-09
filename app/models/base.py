"""
Modelo base para todos los modelos Pydantic
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class BaseModel(BaseModel):
    """Modelo base con configuración común"""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class TimestampMixin(BaseModel):
    """Mixin para campos de timestamp"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class IDMixin(BaseModel):
    """Mixin para campo ID"""
    id: UUID
