"""
Repositorio para la entidad Rol
"""
from typing import List, Optional
from uuid import UUID

from .base import BaseRepository
from app.models.rol import Rol, RolCreate, RolUpdate


class RolRepository(BaseRepository):
    """Repositorio para manejo de roles"""
    
    def __init__(self):
        super().__init__("roles", Rol)
    
    async def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        """Obtener rol por nombre"""
        return await self.get_by_field_single("nombre", nombre)
    
    async def get_activos(self) -> List[Rol]:
        """Obtener todos los roles activos"""
        return await self.get_by_field("activo", True)
    
    async def create_rol(self, rol_data: RolCreate) -> Rol:
        """Crear nuevo rol"""
        return await self.create(rol_data.dict())
    
    async def update_rol(self, rol_id: UUID, rol_data: RolUpdate) -> Optional[Rol]:
        """Actualizar rol"""
        return await self.update(rol_id, rol_data.dict(exclude_unset=True))
    
    async def delete_rol(self, rol_id: UUID) -> bool:
        """Eliminar rol (soft delete)"""
        return await self.update(rol_id, {"activo": False})
