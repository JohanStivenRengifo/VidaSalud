"""
Modelos para la entidad EstadoCita
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class EstadoCitaBase(BasePydanticModel):
    """Modelo base para EstadoCita"""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    color: str = Field(default="#6B7280", pattern=r"^#[0-9A-Fa-f]{6}$")
    orden: int = Field(default=0, ge=0)
    activo: bool = True


class EstadoCitaCreate(EstadoCitaBase):
    """Modelo para crear un estado de cita"""
    pass


class EstadoCitaUpdate(BasePydanticModel):
    """Modelo para actualizar un estado de cita"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    orden: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None


class EstadoCita(EstadoCitaBase, IDMixin, TimestampMixin):
    """Modelo completo de EstadoCita"""
    pass


class EstadoCitaResponse(EstadoCita):
    """Modelo de respuesta para EstadoCita"""
    pass
