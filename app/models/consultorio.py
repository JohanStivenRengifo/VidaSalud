"""
Modelos para la entidad Consultorio
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class ConsultorioBase(BasePydanticModel):
    """Modelo base para Consultorio"""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    ubicacion: Optional[str] = Field(None, max_length=200)
    capacidad: int = Field(default=1, ge=1, le=10)
    equipamiento: Optional[str] = Field(None, max_length=1000)
    activo: bool = True


class ConsultorioCreate(ConsultorioBase):
    """Modelo para crear un consultorio"""
    pass


class ConsultorioUpdate(BasePydanticModel):
    """Modelo para actualizar un consultorio"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    ubicacion: Optional[str] = Field(None, max_length=200)
    capacidad: Optional[int] = Field(None, ge=1, le=10)
    equipamiento: Optional[str] = Field(None, max_length=1000)
    activo: Optional[bool] = None


class Consultorio(ConsultorioBase, IDMixin, TimestampMixin):
    """Modelo completo de Consultorio"""
    pass


class ConsultorioResponse(Consultorio):
    """Modelo de respuesta para Consultorio"""
    pass
