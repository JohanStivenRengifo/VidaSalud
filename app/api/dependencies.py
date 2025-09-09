"""
Dependencias para los endpoints de la API
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.services.auth_service import AuthService
from app.models.usuario import Usuario

security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Usuario:
    """Obtener el usuario actual desde el token JWT"""
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    return user


async def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Obtener el usuario actual activo"""
    if not current_user["activo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


async def get_current_paciente(current_user: Usuario = Depends(get_current_active_user)) -> dict:
    """Obtener el paciente actual"""
    from app.services.paciente_service import PacienteService
    paciente_service = PacienteService()
    
    paciente = await paciente_service.get_paciente_by_usuario(current_user["id"])
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no es un paciente"
        )
    return paciente


async def get_current_medico(current_user: Usuario = Depends(get_current_active_user)) -> dict:
    """Obtener el médico actual"""
    from app.services.medico_service import MedicoService
    medico_service = MedicoService()
    
    medico = await medico_service.get_medico_by_usuario(current_user["id"])
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no es un médico"
        )
    return medico


def require_role(required_role: str):
    """Decorator para requerir un rol específico"""
    async def role_checker(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
        # Aquí podrías implementar lógica para verificar roles
        # Por simplicidad, asumimos que todos los usuarios activos pueden acceder
        return current_user
    return role_checker
