"""
Modelos para la entidad Rol
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class RolBase(BasePydanticModel):
    """Modelo base para Rol"""
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    permisos: List[str] = Field(default_factory=list)
    activo: bool = True


class RolCreate(RolBase):
    """Modelo para crear un rol"""
    pass


class RolUpdate(BasePydanticModel):
    """Modelo para actualizar un rol"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    permisos: Optional[List[str]] = None
    activo: Optional[bool] = None


class Rol(RolBase, IDMixin, TimestampMixin):
    """Modelo completo de Rol"""
    pass


class RolResponse(Rol):
    """Modelo de respuesta para Rol"""
    pass
