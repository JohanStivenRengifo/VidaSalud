"""
Repositorio para la entidad Usuario
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.usuario import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio para operaciones de Usuario"""
    
    def __init__(self, client: Client):
        super().__init__(client, "usuarios")
    
    async def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return await self.get_by_field_single("email", email)
    
    async def get_by_documento(self, documento: str) -> Optional[Usuario]:
        """Obtener usuario por documento de identidad"""
        return await self.get_by_field_single("documento_identidad", documento)
    
    async def get_by_rol(self, rol_id: UUID) -> List[Usuario]:
        """Obtener usuarios por rol"""
        return await self.get_by_field("rol_id", str(rol_id))
    
    async def get_activos(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener usuarios activos"""
        try:
            result = self.client.table(self.table_name).select("*").eq("activo", True).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def update_ultimo_login(self, id: UUID) -> Optional[Usuario]:
        """Actualizar último login del usuario"""
        from datetime import datetime
        data = {"ultimo_login": datetime.utcnow().isoformat()}
        return await self.update(id, data)
    
    async def verify_email(self, id: UUID) -> Optional[Usuario]:
        """Verificar email del usuario"""
        data = {"email_verificado": True}
        return await self.update(id, data)
