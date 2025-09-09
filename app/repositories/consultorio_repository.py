"""
Repositorio para la entidad Consultorio
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.consultorio import Consultorio


class ConsultorioRepository(BaseRepository[Consultorio]):
    """Repositorio para operaciones de Consultorio"""
    
    def __init__(self, client: Client):
        super().__init__(client, "consultorios")
    
    async def get_by_nombre(self, nombre: str) -> Optional[Consultorio]:
        """Obtener consultorio por nombre"""
        return await self.get_by_field_single("nombre", nombre)
    
    async def get_activos(self, skip: int = 0, limit: int = 100) -> List[Consultorio]:
        """Obtener consultorios activos"""
        try:
            result = self.client.table(self.table_name).select("*").eq("activo", True).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_ubicacion(self, ubicacion: str) -> List[Consultorio]:
        """Obtener consultorios por ubicación"""
        try:
            result = self.client.table(self.table_name).select("*").ilike("ubicacion", f"%{ubicacion}%").execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_capacidad_minima(self, capacidad_min: int) -> List[Consultorio]:
        """Obtener consultorios con capacidad mínima"""
        try:
            result = self.client.table(self.table_name).select("*").gte("capacidad", capacidad_min).execute()
            return result.data or []
        except Exception as e:
            raise e
