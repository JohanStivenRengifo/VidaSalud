"""
Modelos para la entidad Notificación
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class TipoNotificacion(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class NotificacionBase(BasePydanticModel):
    """Modelo base para Notificación"""
    titulo: str = Field(..., min_length=1, max_length=200)
    mensaje: str = Field(..., min_length=1, max_length=1000)
    tipo: TipoNotificacion = TipoNotificacion.INFO
    leida: bool = False
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)


class NotificacionCreate(NotificacionBase):
    """Modelo para crear una notificación"""
    usuario_id: UUID
    cita_id: Optional[UUID] = None


class NotificacionUpdate(BasePydanticModel):
    """Modelo para actualizar una notificación"""
    leida: Optional[bool] = None
    data: Optional[Dict[str, Any]] = None


class Notificacion(NotificacionBase, IDMixin, TimestampMixin):
    """Modelo completo de Notificación"""
    usuario_id: UUID
    cita_id: Optional[UUID] = None


class NotificacionResponse(Notificacion):
    """Modelo de respuesta para Notificación"""
    pass
