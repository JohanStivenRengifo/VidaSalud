"""
Repositorio para la entidad Paciente
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.paciente import Paciente


class PacienteRepository(BaseRepository[Paciente]):
    """Repositorio para operaciones de Paciente"""
    
    def __init__(self, client: Client):
        super().__init__(client, "pacientes")
    
    async def get_by_usuario_id(self, usuario_id: UUID) -> Optional[Paciente]:
        """Obtener paciente por usuario_id"""
        return await self.get_by_field_single("usuario_id", str(usuario_id))
    
    async def get_by_seguro_medico(self, seguro: str) -> List[Paciente]:
        """Obtener pacientes por seguro médico"""
        return await self.get_by_field("seguro_medico", seguro)
    
    async def search_by_name(self, nombre: str) -> List[Paciente]:
        """Buscar pacientes por nombre (usando join con usuarios)"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                usuarios!inner(nombre, apellidos)
            """).ilike("usuarios.nombre", f"%{nombre}%").execute()
            return result.data or []
        except Exception as e:
            raise e
