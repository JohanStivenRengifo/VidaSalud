"""
Servicio para la entidad Notificación
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.notificacion import Notificacion, NotificacionCreate, NotificacionUpdate, NotificacionResponse
from app.repositories.notificacion_repository import NotificacionRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.database import db_connection


class NotificacionService:
    """Servicio para operaciones de Notificación"""
    
    def __init__(self):
        self.notificacion_repo = NotificacionRepository(db_connection.client)
        self.usuario_repo = UsuarioRepository(db_connection.client)
    
    async def create_notificacion(self, notificacion_data: NotificacionCreate) -> NotificacionResponse:
        """Crear una nueva notificación"""
        # Verificar que el usuario existe
        usuario = await self.usuario_repo.get_by_id(notificacion_data.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Crear la notificación
        notificacion_dict = notificacion_data.dict()
        created_notificacion = await self.notificacion_repo.create(notificacion_dict)
        if not created_notificacion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la notificación"
            )
        
        return NotificacionResponse(**created_notificacion)
    
    async def get_notificacion(self, notificacion_id: UUID) -> NotificacionResponse:
        """Obtener una notificación por ID"""
        notificacion = await self.notificacion_repo.get_by_id(notificacion_id)
        if not notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificación no encontrada"
            )
        return NotificacionResponse(**notificacion)
    
    async def get_notificaciones(self, skip: int = 0, limit: int = 100) -> List[NotificacionResponse]:
        """Obtener lista de notificaciones"""
        notificaciones = await self.notificacion_repo.get_all(skip, limit)
        return [NotificacionResponse(**notificacion) for notificacion in notificaciones]
    
    async def update_notificacion(self, notificacion_id: UUID, notificacion_data: NotificacionUpdate) -> NotificacionResponse:
        """Actualizar una notificación"""
        existing_notificacion = await self.notificacion_repo.get_by_id(notificacion_id)
        if not existing_notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificación no encontrada"
            )
        
        update_data = notificacion_data.dict(exclude_unset=True)
        updated_notificacion = await self.notificacion_repo.update(notificacion_id, update_data)
        if not updated_notificacion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la notificación"
            )
        
        return NotificacionResponse(**updated_notificacion)
    
    async def delete_notificacion(self, notificacion_id: UUID) -> bool:
        """Eliminar una notificación"""
        existing_notificacion = await self.notificacion_repo.get_by_id(notificacion_id)
        if not existing_notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificación no encontrada"
            )
        
        return await self.notificacion_repo.delete(notificacion_id)
    
    async def get_notificaciones_by_usuario(self, usuario_id: UUID) -> List[NotificacionResponse]:
        """Obtener notificaciones por usuario"""
        notificaciones = await self.notificacion_repo.get_by_usuario(usuario_id)
        return [NotificacionResponse(**notificacion) for notificacion in notificaciones]
    
    async def get_notificaciones_no_leidas(self, usuario_id: UUID) -> List[NotificacionResponse]:
        """Obtener notificaciones no leídas de un usuario"""
        notificaciones = await self.notificacion_repo.get_no_leidas(usuario_id)
        return [NotificacionResponse(**notificacion) for notificacion in notificaciones]
    
    async def get_notificaciones_by_tipo(self, usuario_id: UUID, tipo: str) -> List[NotificacionResponse]:
        """Obtener notificaciones por tipo"""
        notificaciones = await self.notificacion_repo.get_by_tipo(usuario_id, tipo)
        return [NotificacionResponse(**notificacion) for notificacion in notificaciones]
    
    async def marcar_como_leida(self, notificacion_id: UUID) -> NotificacionResponse:
        """Marcar notificación como leída"""
        notificacion = await self.notificacion_repo.marcar_como_leida(notificacion_id)
        if not notificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notificación no encontrada"
            )
        return NotificacionResponse(**notificacion)
    
    async def marcar_todas_como_leidas(self, usuario_id: UUID) -> bool:
        """Marcar todas las notificaciones de un usuario como leídas"""
        return await self.notificacion_repo.marcar_todas_como_leidas(usuario_id)
    
    async def create_notificacion_cita(self, usuario_id: UUID, cita_id: UUID, titulo: str, mensaje: str, tipo: str = "info") -> NotificacionResponse:
        """Crear notificación relacionada con una cita"""
        notificacion_data = NotificacionCreate(
            usuario_id=usuario_id,
            cita_id=cita_id,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo
        )
        return await self.create_notificacion(notificacion_data)
    
    async def create_notificacion_general(self, usuario_id: UUID, titulo: str, mensaje: str, tipo: str = "info") -> NotificacionResponse:
        """Crear notificación general"""
        notificacion_data = NotificacionCreate(
            usuario_id=usuario_id,
            titulo=titulo,
            mensaje=mensaje,
            tipo=tipo
        )
        return await self.create_notificacion(notificacion_data)
