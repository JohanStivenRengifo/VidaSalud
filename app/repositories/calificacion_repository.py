"""
Repositorio para la entidad Calificación
"""
from typing import List, Optional
from uuid import UUID
from supabase import Client

from .base import BaseRepository
from app.models.calificacion import Calificacion


class CalificacionRepository(BaseRepository[Calificacion]):
    """Repositorio para operaciones de Calificación"""
    
    def __init__(self, client: Client):
        super().__init__(client, "calificaciones")
    
    async def get_by_cita(self, cita_id: UUID) -> Optional[Calificacion]:
        """Obtener calificación por cita"""
        return await self.get_by_field_single("cita_id", str(cita_id))
    
    async def get_by_paciente(self, paciente_id: UUID) -> List[Calificacion]:
        """Obtener calificaciones por paciente"""
        return await self.get_by_field("paciente_id", str(paciente_id))
    
    async def get_by_medico(self, medico_id: UUID) -> List[Calificacion]:
        """Obtener calificaciones por médico"""
        return await self.get_by_field("medico_id", str(medico_id))
    
    async def get_promedio_medico(self, medico_id: UUID) -> float:
        """Obtener calificación promedio de un médico"""
        try:
            result = self.client.table(self.table_name).select("calificacion").eq("medico_id", str(medico_id)).execute()
            if result.data:
                calificaciones = [c["calificacion"] for c in result.data]
                return sum(calificaciones) / len(calificaciones)
            return 0.0
        except Exception as e:
            raise e
    
    async def get_with_details(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Obtener calificaciones con información detallada"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                pacientes!inner(usuarios(nombre, apellidos)),
                medicos!inner(usuarios(nombre, apellidos)),
                citas(fecha, hora_inicio)
            """).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
