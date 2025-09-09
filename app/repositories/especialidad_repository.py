"""
Repositorio para la entidad Especialidad
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.especialidad import Especialidad


class EspecialidadRepository(BaseRepository[Especialidad]):
    """Repositorio para operaciones de Especialidad"""
    
    def __init__(self, client: Client):
        super().__init__(client, "especialidades")
    
    async def get_by_nombre(self, nombre: str) -> Optional[Especialidad]:
        """Obtener especialidad por nombre"""
        return await self.get_by_field_single("nombre", nombre)
    
    async def get_activas(self, skip: int = 0, limit: int = 100) -> List[Especialidad]:
        """Obtener especialidades activas"""
        try:
            result = self.client.table(self.table_name).select("*").eq("activo", True).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def search_by_nombre(self, nombre: str) -> List[Especialidad]:
        """Buscar especialidades por nombre"""
        try:
            result = self.client.table(self.table_name).select("*").ilike("nombre", f"%{nombre}%").execute()
            return result.data or []
        except Exception as e:
            raise e
