"""
Modelos para la entidad Usuario
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from enum import Enum

from .base import BaseModel as BasePydanticModel, TimestampMixin, IDMixin


class TipoDocumento(str, Enum):
    CC = "CC"
    CE = "CE"
    PP = "PP"
    TI = "TI"


class Genero(str, Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"
    OTRO = "Otro"
    PREFIERO_NO_DECIR = "Prefiero no decir"


class UsuarioBase(BasePydanticModel):
    """Modelo base para Usuario"""
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    nombre: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Genero] = None
    direccion: Optional[str] = Field(None, max_length=500)
    documento_identidad: Optional[str] = Field(None, max_length=20)
    tipo_documento: Optional[TipoDocumento] = None
    activo: bool = True
    email_verificado: bool = False


class UsuarioCreate(UsuarioBase):
    """Modelo para crear un usuario"""
    password: str = Field(..., min_length=8, max_length=100)
    rol_id: UUID
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una letra mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v


class UsuarioUpdate(BasePydanticModel):
    """Modelo para actualizar un usuario"""
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    genero: Optional[Genero] = None
    direccion: Optional[str] = Field(None, max_length=500)
    documento_identidad: Optional[str] = Field(None, max_length=20)
    tipo_documento: Optional[TipoDocumento] = None
    activo: Optional[bool] = None


class Usuario(UsuarioBase, IDMixin, TimestampMixin):
    """Modelo completo de Usuario"""
    rol_id: UUID
    ultimo_login: Optional[datetime] = None
    avatar_url: Optional[str] = None


class UsuarioResponse(Usuario):
    """Modelo de respuesta para Usuario (sin password)"""
    pass


class UsuarioLogin(BasePydanticModel):
    """Modelo para login de usuario"""
    email: str
    password: str


class Token(BasePydanticModel):
    """Modelo para token de autenticación"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int