"""
Repositorio base con operaciones CRUD genéricas
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Dict, Any
from uuid import UUID
from supabase import Client
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Repositorio base con operaciones CRUD genéricas"""
    
    def __init__(self, client: Client, table_name: str):
        self.client = client
        self.table_name = table_name
    
    async def create(self, data: Dict[str, Any]) -> Optional[T]:
        """Crear un nuevo registro"""
        try:
            result = self.client.table(self.table_name).insert(data).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error al crear registro en {self.table_name}: {e}")
            raise
    
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Obtener un registro por ID"""
        try:
            result = self.client.table(self.table_name).select("*").eq("id", str(id)).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error al obtener registro {id} de {self.table_name}: {e}")
            raise
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtener todos los registros con paginación"""
        try:
            result = self.client.table(self.table_name).select("*").range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error al obtener registros de {self.table_name}: {e}")
            raise
    
    async def update(self, id: UUID, data: Dict[str, Any]) -> Optional[T]:
        """Actualizar un registro"""
        try:
            result = self.client.table(self.table_name).update(data).eq("id", str(id)).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error al actualizar registro {id} en {self.table_name}: {e}")
            raise
    
    async def delete(self, id: UUID) -> bool:
        """Eliminar un registro"""
        try:
            result = self.client.table(self.table_name).delete().eq("id", str(id)).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error al eliminar registro {id} de {self.table_name}: {e}")
            raise
    
    async def get_by_field(self, field: str, value: Any) -> List[T]:
        """Obtener registros por un campo específico"""
        try:
            result = self.client.table(self.table_name).select("*").eq(field, value).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error al obtener registros por {field} de {self.table_name}: {e}")
            raise
    
    async def get_by_field_single(self, field: str, value: Any) -> Optional[T]:
        """Obtener un registro por un campo específico"""
        try:
            result = self.client.table(self.table_name).select("*").eq(field, value).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error al obtener registro por {field} de {self.table_name}: {e}")
            raise
    
    async def count(self) -> int:
        """Contar el número total de registros"""
        try:
            result = self.client.table(self.table_name).select("id", count="exact").execute()
            return result.count or 0
        except Exception as e:
            logger.error(f"Error al contar registros de {self.table_name}: {e}")
            raise
