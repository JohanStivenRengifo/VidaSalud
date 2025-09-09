"""
Repositorio para la entidad Cita
"""
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from supabase import Client

from .base import BaseRepository
from app.models.cita import Cita


class CitaRepository(BaseRepository[Cita]):
    """Repositorio para operaciones de Cita"""
    
    def __init__(self, client: Client):
        super().__init__(client, "citas")
    
    async def get_by_paciente(self, paciente_id: UUID) -> List[Cita]:
        """Obtener citas por paciente"""
        return await self.get_by_field("paciente_id", str(paciente_id))
    
    async def get_by_medico(self, medico_id: UUID) -> List[Cita]:
        """Obtener citas por médico"""
        return await self.get_by_field("medico_id", str(medico_id))
    
    async def get_by_fecha(self, fecha: date) -> List[Cita]:
        """Obtener citas por fecha"""
        return await self.get_by_field("fecha", fecha.isoformat())
    
    async def get_by_estado(self, estado_id: UUID) -> List[Cita]:
        """Obtener citas por estado"""
        return await self.get_by_field("estado_id", str(estado_id))
    
    async def get_by_consultorio(self, consultorio_id: UUID) -> List[Cita]:
        """Obtener citas por consultorio"""
        return await self.get_by_field("consultorio_id", str(consultorio_id))
    
    async def get_by_fecha_range(self, fecha_inicio: date, fecha_fin: date) -> List[Cita]:
        """Obtener citas en un rango de fechas"""
        try:
            result = self.client.table(self.table_name).select("*").gte("fecha", fecha_inicio.isoformat()).lte("fecha", fecha_fin.isoformat()).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_medico_fecha(self, medico_id: UUID, fecha: date) -> List[Cita]:
        """Obtener citas de un médico en una fecha específica"""
        try:
            result = self.client.table(self.table_name).select("*").eq("medico_id", str(medico_id)).eq("fecha", fecha.isoformat()).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_pendientes_pago(self) -> List[Cita]:
        """Obtener citas pendientes de pago"""
        return await self.get_by_field("pagado", False)
    
    async def get_with_details(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Obtener citas con información detallada"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                pacientes!inner(usuarios(nombre, apellidos)),
                medicos!inner(usuarios(nombre, apellidos), especialidades(nombre)),
                consultorios(nombre, ubicacion),
                estados_cita(nombre, color)
            """).range(skip, skip + limit - 1).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_paciente_with_details(self, paciente_id: UUID) -> List[dict]:
        """Obtener citas de un paciente con información detallada"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                medicos!inner(usuarios(nombre, apellidos), especialidades(nombre)),
                consultorios(nombre, ubicacion),
                estados_cita(nombre, color)
            """).eq("paciente_id", str(paciente_id)).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def get_by_medico_with_details(self, medico_id: UUID) -> List[dict]:
        """Obtener citas de un médico con información detallada"""
        try:
            result = self.client.table(self.table_name).select("""
                *,
                pacientes!inner(usuarios(nombre, apellidos)),
                consultorios(nombre, ubicacion),
                estados_cita(nombre, color)
            """).eq("medico_id", str(medico_id)).execute()
            return result.data or []
        except Exception as e:
            raise e
    
    async def check_horario_disponible(self, medico_id: UUID, fecha: date, hora_inicio: str, hora_fin: str) -> bool:
        """Verificar si un horario está disponible para un médico"""
        try:
            result = self.client.table(self.table_name).select("id").eq("medico_id", str(medico_id)).eq("fecha", fecha.isoformat()).or_(f"hora_inicio.lte.{hora_inicio},hora_fin.gte.{hora_fin}").execute()
            return len(result.data) == 0
        except Exception as e:
            raise e
