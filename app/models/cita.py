"""
Modelos para la entidad Cita
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, time, datetime
from uuid import UUID
from decimal import Decimal

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class CitaBase(BasePydanticModel):
    """Modelo base para Cita"""
    fecha: date
    hora_inicio: time
    hora_fin: time
    duracion: Optional[int] = Field(30, ge=1, description="Duración en minutos")
    motivo_consulta: Optional[str] = Field(None, max_length=1000)
    observaciones_medico: Optional[str] = Field(None, max_length=1000)
    diagnostico: Optional[str] = Field(None, max_length=1000)
    tratamiento: Optional[str] = Field(None, max_length=1000)
    medicamentos_recetados: Optional[str] = Field(None, max_length=1000)
    precio: Optional[Decimal] = Field(None, ge=0)
    pagado: bool = False
    recordatorio_enviado: bool = False

    @validator('fecha')
    def validate_fecha(cls, v):
        if v < date.today():
            raise ValueError('La fecha no puede ser anterior a hoy')
        return v

    @validator('hora_fin')
    def validate_hora_fin(cls, v, values):
        if 'hora_inicio' in values and v <= values['hora_inicio']:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return v


class CitaCreate(CitaBase):
    """Modelo para crear una cita"""
    paciente_id: UUID
    medico_id: UUID
    consultorio_id: Optional[UUID] = None
    estado_id: UUID


class CitaUpdate(BasePydanticModel):
    """Modelo para actualizar una cita"""
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    duracion: Optional[int] = Field(None, ge=1)
    consultorio_id: Optional[UUID] = None
    estado_id: Optional[UUID] = None
    motivo_consulta: Optional[str] = Field(None, max_length=1000)
    observaciones_medico: Optional[str] = Field(None, max_length=1000)
    diagnostico: Optional[str] = Field(None, max_length=1000)
    tratamiento: Optional[str] = Field(None, max_length=1000)
    medicamentos_recetados: Optional[str] = Field(None, max_length=1000)
    precio: Optional[Decimal] = Field(None, ge=0)
    pagado: Optional[bool] = None
    recordatorio_enviado: Optional[bool] = None


class Cita(CitaBase, IDMixin, TimestampMixin):
    """Modelo completo de Cita"""
    paciente_id: UUID
    medico_id: UUID
    consultorio_id: Optional[UUID] = None
    estado_id: UUID


class CitaResponse(Cita):
    """Modelo de respuesta para Cita"""
    pass


class CitaConDetalles(CitaResponse):
    """Modelo de cita con información detallada"""
    paciente_nombre: Optional[str] = None
    paciente_apellidos: Optional[str] = None
    medico_nombre: Optional[str] = None
    medico_apellidos: Optional[str] = None
    especialidad_nombre: Optional[str] = None
    consultorio_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
