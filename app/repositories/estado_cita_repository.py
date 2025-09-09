"""
Repositorio para la entidad EstadoCita
"""
from typing import List, Optional
from uuid import UUID

from .base import BaseRepository
from app.models.estado_cita import EstadoCita, EstadoCitaCreate, EstadoCitaUpdate


class EstadoCitaRepository(BaseRepository):
    """Repositorio para manejo de estados de cita"""
    
    def __init__(self):
        super().__init__("estados_cita", EstadoCita)
    
    async def get_by_nombre(self, nombre: str) -> Optional[EstadoCita]:
        """Obtener estado por nombre"""
        return await self.get_by_field_single("nombre", nombre)
    
    async def get_activos(self) -> List[EstadoCita]:
        """Obtener todos los estados activos ordenados por orden"""
        result = self.client.table(self.table_name).select("*").eq("activo", True).order("orden").execute()
        return [self.model_class(**item) for item in result.data] if result.data else []
    
    async def create_estado(self, estado_data: EstadoCitaCreate) -> EstadoCita:
        """Crear nuevo estado"""
        return await self.create(estado_data.dict())
    
    async def update_estado(self, estado_id: UUID, estado_data: EstadoCitaUpdate) -> Optional[EstadoCita]:
        """Actualizar estado"""
        return await self.update(estado_id, estado_data.dict(exclude_unset=True))
    
    async def delete_estado(self, estado_id: UUID) -> bool:
        """Eliminar estado (soft delete)"""
        return await self.update(estado_id, {"activo": False})
