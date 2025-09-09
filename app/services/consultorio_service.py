"""
Servicio para la entidad Consultorio
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.consultorio import Consultorio, ConsultorioCreate, ConsultorioUpdate, ConsultorioResponse
from app.repositories.consultorio_repository import ConsultorioRepository
from app.database import db_connection


class ConsultorioService:
    """Servicio para operaciones de Consultorio"""
    
    def __init__(self):
        self.consultorio_repo = ConsultorioRepository()
    
    async def create_consultorio(self, consultorio_data: ConsultorioCreate) -> ConsultorioResponse:
        """Crear un nuevo consultorio"""
        # Verificar que el nombre no existe
        existing_consultorio = await self.consultorio_repo.get_by_nombre(consultorio_data.nombre)
        if existing_consultorio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del consultorio ya existe"
            )
        
        # Crear el consultorio
        consultorio_dict = consultorio_data.dict()
        created_consultorio = await self.consultorio_repo.create(consultorio_dict)
        if not created_consultorio:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el consultorio"
            )
        
        return ConsultorioResponse(**created_consultorio)
    
    async def get_consultorio(self, consultorio_id: UUID) -> ConsultorioResponse:
        """Obtener un consultorio por ID"""
        consultorio = await self.consultorio_repo.get_by_id(consultorio_id)
        if not consultorio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultorio no encontrado"
            )
        return ConsultorioResponse(**consultorio)
    
    async def get_consultorios(self, skip: int = 0, limit: int = 100) -> List[ConsultorioResponse]:
        """Obtener lista de consultorios"""
        consultorios = await self.consultorio_repo.get_all(skip, limit)
        return [ConsultorioResponse(**consultorio) for consultorio in consultorios]
    
    async def update_consultorio(self, consultorio_id: UUID, consultorio_data: ConsultorioUpdate) -> ConsultorioResponse:
        """Actualizar un consultorio"""
        existing_consultorio = await self.consultorio_repo.get_by_id(consultorio_id)
        if not existing_consultorio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultorio no encontrado"
            )
        
        # Verificar nombre único si se está actualizando
        if (consultorio_data.nombre and 
            consultorio_data.nombre != existing_consultorio["nombre"]):
            nombre_exists = await self.consultorio_repo.get_by_nombre(consultorio_data.nombre)
            if nombre_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre del consultorio ya existe"
                )
        
        update_data = consultorio_data.dict(exclude_unset=True)
        updated_consultorio = await self.consultorio_repo.update(consultorio_id, update_data)
        if not updated_consultorio:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el consultorio"
            )
        
        return ConsultorioResponse(**updated_consultorio)
    
    async def delete_consultorio(self, consultorio_id: UUID) -> bool:
        """Eliminar un consultorio (soft delete)"""
        existing_consultorio = await self.consultorio_repo.get_by_id(consultorio_id)
        if not existing_consultorio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consultorio no encontrado"
            )
        
        # Soft delete - marcar como inactivo
        update_data = {"activo": False}
        updated_consultorio = await self.consultorio_repo.update(consultorio_id, update_data)
        return updated_consultorio is not None
    
    async def get_consultorios_activos(self, skip: int = 0, limit: int = 100) -> List[ConsultorioResponse]:
        """Obtener consultorios activos"""
        consultorios = await self.consultorio_repo.get_activos(skip, limit)
        return [ConsultorioResponse(**consultorio) for consultorio in consultorios]
    
    async def get_consultorios_by_ubicacion(self, ubicacion: str) -> List[ConsultorioResponse]:
        """Obtener consultorios por ubicación"""
        consultorios = await self.consultorio_repo.get_by_ubicacion(ubicacion)
        return [ConsultorioResponse(**consultorio) for consultorio in consultorios]
    
    async def get_consultorios_by_capacidad(self, capacidad_min: int) -> List[ConsultorioResponse]:
        """Obtener consultorios con capacidad mínima"""
        consultorios = await self.consultorio_repo.get_by_capacidad_minima(capacidad_min)
        return [ConsultorioResponse(**consultorio) for consultorio in consultorios]
