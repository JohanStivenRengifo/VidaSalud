"""
Modelos para la entidad Calificación
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class CalificacionBase(BasePydanticModel):
    """Modelo base para Calificación"""
    calificacion: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = Field(None, max_length=1000)

    @validator('calificacion')
    def validate_calificacion(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('La calificación debe estar entre 1 y 5')
        return v


class CalificacionCreate(CalificacionBase):
    """Modelo para crear una calificación"""
    cita_id: UUID
    paciente_id: UUID
    medico_id: UUID


class CalificacionUpdate(BasePydanticModel):
    """Modelo para actualizar una calificación"""
    calificacion: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = Field(None, max_length=1000)


class Calificacion(CalificacionBase, IDMixin, TimestampMixin):
    """Modelo completo de Calificación"""
    cita_id: UUID
    paciente_id: UUID
    medico_id: UUID


class CalificacionResponse(Calificacion):
    """Modelo de respuesta para Calificación"""
    pass


class CalificacionConDetalles(CalificacionResponse):
    """Modelo de calificación con información detallada"""
    paciente_nombre: Optional[str] = None
    paciente_apellidos: Optional[str] = None
    medico_nombre: Optional[str] = None
    medico_apellidos: Optional[str] = None
    cita_fecha: Optional[datetime] = None
