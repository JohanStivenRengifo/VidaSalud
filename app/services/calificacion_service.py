"""
Servicio para la entidad Calificación
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.calificacion import Calificacion, CalificacionCreate, CalificacionUpdate, CalificacionResponse, CalificacionConDetalles
from app.repositories.calificacion_repository import CalificacionRepository
from app.repositories.cita_repository import CitaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository
from app.database import db_connection


class CalificacionService:
    """Servicio para operaciones de Calificación"""
    
    def __init__(self):
        self.calificacion_repo = CalificacionRepository()
        self.cita_repo = CitaRepository()
        self.medico_repo = MedicoRepository()
        self.paciente_repo = PacienteRepository()
    
    async def create_calificacion(self, calificacion_data: CalificacionCreate) -> CalificacionResponse:
        """Crear una nueva calificación"""
        # Verificar que la cita existe
        cita = await self.cita_repo.get_by_id(calificacion_data.cita_id)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        
        # Verificar que el paciente existe
        paciente = await self.paciente_repo.get_by_id(calificacion_data.paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        # Verificar que el médico existe
        medico = await self.medico_repo.get_by_id(calificacion_data.medico_id)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        # Verificar que no existe ya una calificación para esta cita
        existing_calificacion = await self.calificacion_repo.get_by_cita(calificacion_data.cita_id)
        if existing_calificacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una calificación para esta cita"
            )
        
        # Verificar que la cita pertenece al paciente
        if cita["paciente_id"] != calificacion_data.paciente_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cita no pertenece al paciente"
            )
        
        # Verificar que la cita pertenece al médico
        if cita["medico_id"] != calificacion_data.medico_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cita no pertenece al médico"
            )
        
        # Crear la calificación
        calificacion_dict = calificacion_data.dict()
        created_calificacion = await self.calificacion_repo.create(calificacion_dict)
        if not created_calificacion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la calificación"
            )
        
        # Actualizar calificación promedio del médico
        from app.services.medico_service import MedicoService
        medico_service = MedicoService()
        await medico_service.update_calificacion_promedio(calificacion_data.medico_id)
        
        return CalificacionResponse(**created_calificacion)
    
    async def get_calificacion(self, calificacion_id: UUID) -> CalificacionResponse:
        """Obtener una calificación por ID"""
        calificacion = await self.calificacion_repo.get_by_id(calificacion_id)
        if not calificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calificación no encontrada"
            )
        return CalificacionResponse(**calificacion)
    
    async def get_calificaciones(self, skip: int = 0, limit: int = 100) -> List[CalificacionResponse]:
        """Obtener lista de calificaciones"""
        calificaciones = await self.calificacion_repo.get_all(skip, limit)
        return [CalificacionResponse(**calificacion) for calificacion in calificaciones]
    
    async def get_calificaciones_with_details(self, skip: int = 0, limit: int = 100) -> List[CalificacionConDetalles]:
        """Obtener calificaciones con información detallada"""
        calificaciones = await self.calificacion_repo.get_with_details(skip, limit)
        return [CalificacionConDetalles(**calificacion) for calificacion in calificaciones]
    
    async def update_calificacion(self, calificacion_id: UUID, calificacion_data: CalificacionUpdate) -> CalificacionResponse:
        """Actualizar una calificación"""
        existing_calificacion = await self.calificacion_repo.get_by_id(calificacion_id)
        if not existing_calificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calificación no encontrada"
            )
        
        update_data = calificacion_data.dict(exclude_unset=True)
        updated_calificacion = await self.calificacion_repo.update(calificacion_id, update_data)
        if not updated_calificacion:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la calificación"
            )
        
        # Actualizar calificación promedio del médico
        from app.services.medico_service import MedicoService
        medico_service = MedicoService()
        await medico_service.update_calificacion_promedio(existing_calificacion["medico_id"])
        
        return CalificacionResponse(**updated_calificacion)
    
    async def delete_calificacion(self, calificacion_id: UUID) -> bool:
        """Eliminar una calificación"""
        existing_calificacion = await self.calificacion_repo.get_by_id(calificacion_id)
        if not existing_calificacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calificación no encontrada"
            )
        
        medico_id = existing_calificacion["medico_id"]
        deleted = await self.calificacion_repo.delete(calificacion_id)
        
        if deleted:
            # Actualizar calificación promedio del médico
            from app.services.medico_service import MedicoService
            medico_service = MedicoService()
            await medico_service.update_calificacion_promedio(medico_id)
        
        return deleted
    
    async def get_calificaciones_by_paciente(self, paciente_id: UUID) -> List[CalificacionResponse]:
        """Obtener calificaciones por paciente"""
        calificaciones = await self.calificacion_repo.get_by_paciente(paciente_id)
        return [CalificacionResponse(**calificacion) for calificacion in calificaciones]
    
    async def get_calificaciones_by_medico(self, medico_id: UUID) -> List[CalificacionResponse]:
        """Obtener calificaciones por médico"""
        calificaciones = await self.calificacion_repo.get_by_medico(medico_id)
        return [CalificacionResponse(**calificacion) for calificacion in calificaciones]
    
    async def get_calificacion_by_cita(self, cita_id: UUID) -> Optional[CalificacionResponse]:
        """Obtener calificación por cita"""
        calificacion = await self.calificacion_repo.get_by_cita(cita_id)
        if calificacion:
            return CalificacionResponse(**calificacion)
        return None
    
    async def get_promedio_medico(self, medico_id: UUID) -> float:
        """Obtener calificación promedio de un médico"""
        return await self.calificacion_repo.get_promedio_medico(medico_id)
