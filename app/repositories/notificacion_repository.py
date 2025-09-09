"""
Repositorio para la entidad Notificación
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.notificacion import Notificacion


class NotificacionRepository(BaseRepository[Notificacion]):
    """Repositorio para operaciones de Notificación"""
    
    def __init__(self, client: Client):
        super().__init__(client, "notificaciones")
    
    async def get_by_usuario(self, usuario_id: UUID) -> List[Notificacion]:
        """Obtener notificaciones por usuario"""
        return await self.get_by_field("usuario_id", str(usuario_id))
    
    async def get_by_cita(self, cita_id: UUID) -> List[Notificacion]:
        """Obtener notificaciones por cita"""
        return await self.get_by_field("cita_id", str(cita_id))
    
    async def get_no_leidas(self, usuario_id: UUID) -> List[Notificacion]:
        """Obtener notificaciones no leídas de un usuario"""
        try:
            result = self.client.table(self.table_name).select("*").eq("usuario_id", str(usuario_id)).eq("leida", False).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_tipo(self, usuario_id: UUID, tipo: str) -> List[Notificacion]:
        """Obtener notificaciones por tipo"""
        try:
            result = self.client.table(self.table_name).select("*").eq("usuario_id", str(usuario_id)).eq("tipo", tipo).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def marcar_como_leida(self, id: UUID) -> Optional[Notificacion]:
        """Marcar notificación como leída"""
        data = {"leida": True}
        return await self.update(id, data)
    
    async def marcar_todas_como_leidas(self, usuario_id: UUID) -> bool:
        """Marcar todas las notificaciones de un usuario como leídas"""
        try:
            result = self.client.table(self.table_name).update({"leida": True}).eq("usuario_id", str(usuario_id)).execute()
            return True
        except Exception as e:
            raise e
