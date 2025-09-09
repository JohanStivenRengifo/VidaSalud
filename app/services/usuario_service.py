"""
Servicio para la entidad Usuario
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auth_service import AuthService
from app.database import db_connection


class UsuarioService:
    """Servicio para operaciones de Usuario"""
    
    def __init__(self):
        self.usuario_repo = UsuarioRepository(db_connection.client)
        self.auth_service = AuthService()
    
    async def create_usuario(self, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """Crear un nuevo usuario usando Supabase Auth"""
        # Verificar si el email ya existe
        existing_user = await self.usuario_repo.get_by_email(usuario_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Verificar si el documento ya existe
        if usuario_data.documento_identidad:
            existing_doc = await self.usuario_repo.get_by_documento(usuario_data.documento_identidad)
            if existing_doc:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El documento de identidad ya está registrado"
                )
        
        # Crear el usuario usando Supabase Auth
        try:
            # Registrar en Supabase Auth
            auth_response = await self.auth_service.register(
                email=usuario_data.email,
                password=usuario_data.password,
                user_data={
                    "nombre": usuario_data.nombre,
                    "apellidos": usuario_data.apellidos,
                    "documento_identidad": usuario_data.documento_identidad,
                    "telefono": usuario_data.telefono,
                    "rol_id": str(usuario_data.rol_id),
                    "activo": True
                }
            )
            
            # Obtener el usuario creado
            created_user = await self.usuario_repo.get_by_id(auth_response.user_id)
            if not created_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al obtener el usuario creado"
                )
            
            return UsuarioResponse(**created_user)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el usuario: {str(e)}"
            )
    
    async def get_usuario(self, usuario_id: UUID) -> UsuarioResponse:
        """Obtener un usuario por ID"""
        usuario = await self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return UsuarioResponse(**usuario)
    
    async def get_usuarios(self, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        """Obtener lista de usuarios"""
        usuarios = await self.usuario_repo.get_all(skip, limit)
        return [UsuarioResponse(**usuario) for usuario in usuarios]
    
    async def update_usuario(self, usuario_id: UUID, usuario_data: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar un usuario"""
        # Verificar si el usuario existe
        existing_user = await self.usuario_repo.get_by_id(usuario_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar email único si se está actualizando
        if usuario_data.email and usuario_data.email != existing_user["email"]:
            email_exists = await self.usuario_repo.get_by_email(usuario_data.email)
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
        
        # Verificar documento único si se está actualizando
        if (usuario_data.documento_identidad and 
            usuario_data.documento_identidad != existing_user.get("documento_identidad")):
            doc_exists = await self.usuario_repo.get_by_documento(usuario_data.documento_identidad)
            if doc_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El documento de identidad ya está registrado"
                )
        
        # Actualizar usuario
        update_data = usuario_data.dict(exclude_unset=True)
        updated_user = await self.usuario_repo.update(usuario_id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el usuario"
            )
        
        return UsuarioResponse(**updated_user)
    
    async def delete_usuario(self, usuario_id: UUID) -> bool:
        """Eliminar un usuario (soft delete)"""
        existing_user = await self.usuario_repo.get_by_id(usuario_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Soft delete - marcar como inactivo
        update_data = {"activo": False}
        updated_user = await self.usuario_repo.update(usuario_id, update_data)
        return updated_user is not None
    
    async def get_usuario_by_email(self, email: str) -> Optional[UsuarioResponse]:
        """Obtener usuario por email"""
        usuario = await self.usuario_repo.get_by_email(email)
        if usuario:
            return UsuarioResponse(**usuario)
        return None
    
    async def verify_email(self, usuario_id: UUID) -> UsuarioResponse:
        """Verificar email del usuario"""
        usuario = await self.usuario_repo.verify_email(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return UsuarioResponse(**usuario)
    
    async def get_usuarios_by_rol(self, rol_id: UUID) -> List[UsuarioResponse]:
        """Obtener usuarios por rol"""
        usuarios = await self.usuario_repo.get_by_rol(rol_id)
        return [UsuarioResponse(**usuario) for usuario in usuarios]
    
    async def get_usuarios_activos(self, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        """Obtener usuarios activos"""
        usuarios = await self.usuario_repo.get_activos(skip, limit)
        return [UsuarioResponse(**usuario) for usuario in usuarios]
