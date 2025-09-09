"""
Modelos para la entidad Médico
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class MedicoBase(BasePydanticModel):
    """Modelo base para Médico"""
    numero_licencia: str = Field(..., min_length=5, max_length=50)
    universidad: Optional[str] = Field(None, max_length=200)
    anos_experiencia: Optional[int] = Field(None, ge=0, le=50)
    biografia: Optional[str] = Field(None, max_length=2000)
    precio_consulta: Optional[Decimal] = Field(None, ge=0)
    disponible: bool = True


class MedicoCreate(MedicoBase):
    """Modelo para crear un médico"""
    usuario_id: UUID
    especialidad_id: UUID


class MedicoUpdate(BasePydanticModel):
    """Modelo para actualizar un médico"""
    numero_licencia: Optional[str] = Field(None, min_length=5, max_length=50)
    universidad: Optional[str] = Field(None, max_length=200)
    anos_experiencia: Optional[int] = Field(None, ge=0, le=50)
    biografia: Optional[str] = Field(None, max_length=2000)
    precio_consulta: Optional[Decimal] = Field(None, ge=0)
    disponible: Optional[bool] = None


class Medico(MedicoBase, IDMixin, TimestampMixin):
    """Modelo completo de Médico"""
    usuario_id: UUID
    especialidad_id: UUID
    calificacion_promedio: Decimal = Field(default=Decimal('0.00'), ge=0, le=5)
    total_consultas: int = 0


class MedicoResponse(Medico):
    """Modelo de respuesta para Médico"""
    pass


class MedicoConEspecialidad(MedicoResponse):
    """Modelo de médico con información de especialidad"""
    especialidad_nombre: Optional[str] = None
    especialidad_descripcion: Optional[str] = None
