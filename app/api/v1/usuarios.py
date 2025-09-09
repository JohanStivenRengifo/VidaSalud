"""
Endpoints para la gestión de usuarios
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import UsuarioService
from app.api.dependencies import get_current_user, require_role

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

usuario_service = UsuarioService()


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
async def create_usuario(usuario_data: UsuarioCreate):
    """
    Crear un nuevo usuario
    
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 8 caracteres, debe incluir mayúsculas, minúsculas y números)
    - **nombre**: Nombre del usuario
    - **apellidos**: Apellidos del usuario
    - **telefono**: Teléfono del usuario (opcional)
    - **fecha_nacimiento**: Fecha de nacimiento (opcional)
    - **genero**: Género del usuario (opcional)
    - **direccion**: Dirección del usuario (opcional)
    - **documento_identidad**: Documento de identidad único (opcional)
    - **tipo_documento**: Tipo de documento (opcional)
    - **rol_id**: ID del rol del usuario
    """
    return await usuario_service.create_usuario(usuario_data)


@router.get("/", response_model=List[UsuarioResponse], summary="Listar usuarios")
async def get_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de usuarios con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await usuario_service.get_usuarios(skip, limit)


@router.get("/activos", response_model=List[UsuarioResponse], summary="Listar usuarios activos")
async def get_usuarios_activos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de usuarios activos con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await usuario_service.get_usuarios_activos(skip, limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse, summary="Obtener usuario por ID")
async def get_usuario(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener un usuario específico por su ID
    
    - **usuario_id**: ID único del usuario
    
    Requiere autenticación
    """
    return await usuario_service.get_usuario(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse, summary="Actualizar usuario")
async def update_usuario(
    usuario_id: UUID,
    usuario_data: UsuarioUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de un usuario
    
    - **usuario_id**: ID único del usuario
    - **usuario_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await usuario_service.update_usuario(usuario_id, usuario_data)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
async def delete_usuario(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar un usuario (soft delete - marca como inactivo)
    
    - **usuario_id**: ID único del usuario
    
    Requiere autenticación
    """
    await usuario_service.delete_usuario(usuario_id)


@router.get("/email/{email}", response_model=UsuarioResponse, summary="Obtener usuario por email")
async def get_usuario_by_email(
    email: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener un usuario por su email
    
    - **email**: Email del usuario
    
    Requiere autenticación
    """
    usuario = await usuario_service.get_usuario_by_email(email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.get("/rol/{rol_id}", response_model=List[UsuarioResponse], summary="Obtener usuarios por rol")
async def get_usuarios_by_rol(
    rol_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener usuarios por rol
    
    - **rol_id**: ID del rol
    
    Requiere autenticación
    """
    return await usuario_service.get_usuarios_by_rol(rol_id)
