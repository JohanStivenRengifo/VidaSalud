"""
Servicio para la entidad Especialidad
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.especialidad import Especialidad, EspecialidadCreate, EspecialidadUpdate, EspecialidadResponse
from app.repositories.especialidad_repository import EspecialidadRepository
from app.database import db_connection


class EspecialidadService:
    """Servicio para operaciones de Especialidad"""
    
    def __init__(self):
        self.especialidad_repo = EspecialidadRepository(db_connection.client)
    
    async def create_especialidad(self, especialidad_data: EspecialidadCreate) -> EspecialidadResponse:
        """Crear una nueva especialidad"""
        # Verificar que el nombre no existe
        existing_especialidad = await self.especialidad_repo.get_by_nombre(especialidad_data.nombre)
        if existing_especialidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la especialidad ya existe"
            )
        
        # Crear la especialidad
        especialidad_dict = especialidad_data.dict()
        created_especialidad = await self.especialidad_repo.create(especialidad_dict)
        if not created_especialidad:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la especialidad"
            )
        
        return EspecialidadResponse(**created_especialidad)
    
    async def get_especialidad(self, especialidad_id: UUID) -> EspecialidadResponse:
        """Obtener una especialidad por ID"""
        especialidad = await self.especialidad_repo.get_by_id(especialidad_id)
        if not especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada"
            )
        return EspecialidadResponse(**especialidad)
    
    async def get_especialidades(self, skip: int = 0, limit: int = 100) -> List[EspecialidadResponse]:
        """Obtener lista de especialidades"""
        especialidades = await self.especialidad_repo.get_all(skip, limit)
        return [EspecialidadResponse(**especialidad) for especialidad in especialidades]
    
    async def update_especialidad(self, especialidad_id: UUID, especialidad_data: EspecialidadUpdate) -> EspecialidadResponse:
        """Actualizar una especialidad"""
        existing_especialidad = await self.especialidad_repo.get_by_id(especialidad_id)
        if not existing_especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada"
            )
        
        # Verificar nombre único si se está actualizando
        if (especialidad_data.nombre and 
            especialidad_data.nombre != existing_especialidad["nombre"]):
            nombre_exists = await self.especialidad_repo.get_by_nombre(especialidad_data.nombre)
            if nombre_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de la especialidad ya existe"
                )
        
        update_data = especialidad_data.dict(exclude_unset=True)
        updated_especialidad = await self.especialidad_repo.update(especialidad_id, update_data)
        if not updated_especialidad:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la especialidad"
            )
        
        return EspecialidadResponse(**updated_especialidad)
    
    async def delete_especialidad(self, especialidad_id: UUID) -> bool:
        """Eliminar una especialidad (soft delete)"""
        existing_especialidad = await self.especialidad_repo.get_by_id(especialidad_id)
        if not existing_especialidad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Especialidad no encontrada"
            )
        
        # Soft delete - marcar como inactiva
        update_data = {"activo": False}
        updated_especialidad = await self.especialidad_repo.update(especialidad_id, update_data)
        return updated_especialidad is not None
    
    async def get_especialidades_activas(self, skip: int = 0, limit: int = 100) -> List[EspecialidadResponse]:
        """Obtener especialidades activas"""
        especialidades = await self.especialidad_repo.get_activas(skip, limit)
        return [EspecialidadResponse(**especialidad) for especialidad in especialidades]
    
    async def search_especialidades(self, nombre: str) -> List[EspecialidadResponse]:
        """Buscar especialidades por nombre"""
        especialidades = await self.especialidad_repo.search_by_nombre(nombre)
        return [EspecialidadResponse(**especialidad) for especialidad in especialidades]
