"""
Servicio para la entidad Médico
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.medico import Medico, MedicoCreate, MedicoUpdate, MedicoResponse, MedicoConEspecialidad
from app.repositories.medico_repository import MedicoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.especialidad_repository import EspecialidadRepository
from app.database import db_connection


class MedicoService:
    """Servicio para operaciones de Médico"""
    
    def __init__(self):
        self.medico_repo = MedicoRepository()
        self.usuario_repo = UsuarioRepository()
        self.especialidad_repo = EspecialidadRepository()
    
    async def create_medico(self, medico_data: MedicoCreate) -> MedicoResponse:
        """Crear un nuevo médico"""
        # Verificar que el usuario existe
        usuario = await self.usuario_repo.get_by_id(medico_data.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar que la especialidad existe
        especialidad = await self.especialidad_repo.get_by_id(medico_data.especialidad_id)
        if not especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada"
            )
        
        # Verificar que el número de licencia es único
        existing_licencia = await self.medico_repo.get_by_licencia(medico_data.numero_licencia)
        if existing_licencia:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de licencia ya está registrado"
            )
        
        # Crear el médico
        medico_dict = medico_data.dict()
        created_medico = await self.medico_repo.create(medico_dict)
        if not created_medico:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el médico"
            )
        
        return MedicoResponse(**created_medico)
    
    async def get_medico(self, medico_id: UUID) -> MedicoResponse:
        """Obtener un médico por ID"""
        medico = await self.medico_repo.get_by_id(medico_id)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        return MedicoResponse(**medico)
    
    async def get_medicos(self, skip: int = 0, limit: int = 100) -> List[MedicoResponse]:
        """Obtener lista de médicos"""
        medicos = await self.medico_repo.get_all(skip, limit)
        return [MedicoResponse(**medico) for medico in medicos]
    
    async def get_medicos_with_especialidad(self, skip: int = 0, limit: int = 100) -> List[MedicoConEspecialidad]:
        """Obtener médicos con información de especialidad"""
        medicos = await self.medico_repo.get_with_especialidad(skip, limit)
        return [MedicoConEspecialidad(**medico) for medico in medicos]
    
    async def update_medico(self, medico_id: UUID, medico_data: MedicoUpdate) -> MedicoResponse:
        """Actualizar un médico"""
        existing_medico = await self.medico_repo.get_by_id(medico_id)
        if not existing_medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        # Verificar número de licencia único si se está actualizando
        if (medico_data.numero_licencia and 
            medico_data.numero_licencia != existing_medico["numero_licencia"]):
            licencia_exists = await self.medico_repo.get_by_licencia(medico_data.numero_licencia)
            if licencia_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El número de licencia ya está registrado"
                )
        
        update_data = medico_data.dict(exclude_unset=True)
        updated_medico = await self.medico_repo.update(medico_id, update_data)
        if not updated_medico:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el médico"
            )
        
        return MedicoResponse(**updated_medico)
    
    async def delete_medico(self, medico_id: UUID) -> bool:
        """Eliminar un médico (soft delete)"""
        existing_medico = await self.medico_repo.get_by_id(medico_id)
        if not existing_medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        # Soft delete - marcar como no disponible
        update_data = {"disponible": False}
        updated_medico = await self.medico_repo.update(medico_id, update_data)
        return updated_medico is not None
    
    async def get_medico_by_usuario(self, usuario_id: UUID) -> Optional[MedicoResponse]:
        """Obtener médico por usuario_id"""
        medico = await self.medico_repo.get_by_usuario_id(usuario_id)
        if medico:
            return MedicoResponse(**medico)
        return None
    
    async def get_medicos_by_especialidad(self, especialidad_id: UUID) -> List[MedicoResponse]:
        """Obtener médicos por especialidad"""
        medicos = await self.medico_repo.get_by_especialidad(especialidad_id)
        return [MedicoResponse(**medico) for medico in medicos]
    
    async def get_medicos_disponibles(self, skip: int = 0, limit: int = 100) -> List[MedicoResponse]:
        """Obtener médicos disponibles"""
        medicos = await self.medico_repo.get_disponibles(skip, limit)
        return [MedicoResponse(**medico) for medico in medicos]
    
    async def get_medicos_by_calificacion(self, calificacion_min: float) -> List[MedicoResponse]:
        """Obtener médicos con calificación mínima"""
        medicos = await self.medico_repo.get_by_calificacion_minima(calificacion_min)
        return [MedicoResponse(**medico) for medico in medicos]
    
    async def update_calificacion_promedio(self, medico_id: UUID) -> MedicoResponse:
        """Actualizar calificación promedio del médico"""
        # Obtener todas las calificaciones del médico
        from app.repositories.calificacion_repository import CalificacionRepository
        calificacion_repo = CalificacionRepository()
        
        calificaciones = await calificacion_repo.get_by_medico(medico_id)
        if not calificaciones:
            # Si no hay calificaciones, mantener en 0
            nueva_calificacion = 0.0
        else:
            # Calcular promedio
            suma_calificaciones = sum(cal["calificacion"] for cal in calificaciones)
            nueva_calificacion = suma_calificaciones / len(calificaciones)
        
        updated_medico = await self.medico_repo.update_calificacion_promedio(medico_id, nueva_calificacion)
        if not updated_medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        return MedicoResponse(**updated_medico)
    
    async def incrementar_consultas(self, medico_id: UUID) -> MedicoResponse:
        """Incrementar contador de consultas del médico"""
        updated_medico = await self.medico_repo.incrementar_consultas(medico_id)
        if not updated_medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        return MedicoResponse(**updated_medico)
