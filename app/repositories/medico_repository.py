"""
Repositorio para la entidad Médico
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.medico import Medico


class MedicoRepository(BaseRepository[Medico]):
    """Repositorio para operaciones de Médico"""
    
    def __init__(self, client: Client):
        super().__init__(client, "medicos")
    
    async def get_by_usuario_id(self, usuario_id: UUID) -> Optional[Medico]:
        """Obtener médico por usuario_id"""
        return await self.get_by_field_single("usuario_id", str(usuario_id))
    
    async def get_by_especialidad(self, especialidad_id: UUID) -> List[Medico]:
        """Obtener médicos por especialidad"""
        return await self.get_by_field("especialidad_id", str(especialidad_id))
    
    async def get_by_licencia(self, numero_licencia: str) -> Optional[Medico]:
        """Obtener médico por número de licencia"""
        return await self.get_by_field_single("numero_licencia", numero_licencia)
    
    async def get_disponibles(self, skip: int = 0, limit: int = 100) -> List[Medico]:
        """Obtener médicos disponibles"""
        try:
            result = self.client.table(self.table_name).select("*").eq("disponible", True).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_calificacion_minima(self, calificacion_min: float) -> List[Medico]:
        """Obtener médicos con calificación mínima"""
        try:
            result = self.client.table(self.table_name).select("*").gte("calificacion_promedio", calificacion_min).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_with_especialidad(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Obtener médicos con información de especialidad"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                especialidades(nombre, descripcion),
                usuarios(nombre, apellidos, telefono)
            """).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def update_calificacion_promedio(self, id: UUID, nueva_calificacion: float) -> Optional[Medico]:
        """Actualizar calificación promedio del médico"""
        data = {"calificacion_promedio": nueva_calificacion}
        return await self.update(id, data)
    
    async def incrementar_consultas(self, id: UUID) -> Optional[Medico]:
        """Incrementar contador de consultas del médico"""
        try:
            # Primero obtenemos el médico actual
            medico = await self.get_by_id(id)
            if medico:
                total_consultas = medico.get("total_consultas", 0) + 1
                data = {"total_consultas": total_consultas}
                return await self.update(id, data)
            return None
        except Exception as e:
            raise e
