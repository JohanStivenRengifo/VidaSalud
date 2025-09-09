"""
Modelos para la entidad Paciente
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class PacienteBase(BasePydanticModel):
    """Modelo base para Paciente"""
    tipo_sangre: Optional[str] = Field(None, max_length=10)
    alergias: Optional[str] = Field(None, max_length=1000)
    enfermedades_cronicas: Optional[str] = Field(None, max_length=1000)
    medicamentos_actuales: Optional[str] = Field(None, max_length=1000)
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=100)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=20)
    seguro_medico: Optional[str] = Field(None, max_length=100)
    numero_seguro: Optional[str] = Field(None, max_length=50)


class PacienteCreate(PacienteBase):
    """Modelo para crear un paciente"""
    usuario_id: UUID


class PacienteUpdate(BasePydanticModel):
    """Modelo para actualizar un paciente"""
    tipo_sangre: Optional[str] = Field(None, max_length=10)
    alergias: Optional[str] = Field(None, max_length=1000)
    enfermedades_cronicas: Optional[str] = Field(None, max_length=1000)
    medicamentos_actuales: Optional[str] = Field(None, max_length=1000)
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=100)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=20)
    seguro_medico: Optional[str] = Field(None, max_length=100)
    numero_seguro: Optional[str] = Field(None, max_length=50)


class Paciente(PacienteBase, IDMixin, TimestampMixin):
    """Modelo completo de Paciente"""
    usuario_id: UUID


class PacienteResponse(Paciente):
    """Modelo de respuesta para Paciente"""
    pass
