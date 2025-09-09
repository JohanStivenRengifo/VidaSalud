"""
Modelos para la entidad Especialidad
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class EspecialidadBase(BasePydanticModel):
    """Modelo base para Especialidad"""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    duracion_cita_default: int = Field(default=30, ge=15, le=180)
    precio_base: Optional[Decimal] = Field(None, ge=0)
    activo: bool = True


class EspecialidadCreate(EspecialidadBase):
    """Modelo para crear una especialidad"""
    pass


class EspecialidadUpdate(BasePydanticModel):
    """Modelo para actualizar una especialidad"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    duracion_cita_default: Optional[int] = Field(None, ge=15, le=180)
    precio_base: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None


class Especialidad(EspecialidadBase, IDMixin, TimestampMixin):
    """Modelo completo de Especialidad"""
    pass


class EspecialidadResponse(Especialidad):
    """Modelo de respuesta para Especialidad"""
    pass
