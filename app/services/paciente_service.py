"""
Servicio para la entidad Paciente
"""
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status

from app.models.paciente import Paciente, PacienteCreate, PacienteUpdate, PacienteResponse
from app.repositories.paciente_repository import PacienteRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.database import db_connection


class PacienteService:
    """Servicio para operaciones de Paciente"""
    
    def __init__(self):
        self.paciente_repo = PacienteRepository()
        self.usuario_repo = UsuarioRepository()
    
    async def create_paciente(self, paciente_data: PacienteCreate) -> PacienteResponse:
        """Crear un nuevo paciente"""
        # Verificar que el usuario existe
        usuario = await self.usuario_repo.get_by_id(paciente_data.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar que el usuario no sea ya un paciente
        existing_paciente = await self.paciente_repo.get_by_usuario_id(paciente_data.usuario_id)
        if existing_paciente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya es un paciente"
            )
        
        # Crear el paciente
        paciente_dict = paciente_data.dict()
        created_paciente = await self.paciente_repo.create(paciente_dict)
        if not created_paciente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear el paciente"
            )
        
        return PacienteResponse(**created_paciente)
    
    async def get_paciente(self, paciente_id: UUID) -> PacienteResponse:
        """Obtener un paciente por ID"""
        paciente = await self.paciente_repo.get_by_id(paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        return PacienteResponse(**paciente)
    
    async def get_pacientes(self, skip: int = 0, limit: int = 100) -> List[PacienteResponse]:
        """Obtener lista de pacientes"""
        pacientes = await self.paciente_repo.get_all(skip, limit)
        return [PacienteResponse(**paciente) for paciente in pacientes]
    
    async def update_paciente(self, paciente_id: UUID, paciente_data: PacienteUpdate) -> PacienteResponse:
        """Actualizar un paciente"""
        existing_paciente = await self.paciente_repo.get_by_id(paciente_id)
        if not existing_paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        update_data = paciente_data.dict(exclude_unset=True)
        updated_paciente = await self.paciente_repo.update(paciente_id, update_data)
        if not updated_paciente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el paciente"
            )
        
        return PacienteResponse(**updated_paciente)
    
    async def delete_paciente(self, paciente_id: UUID) -> bool:
        """Eliminar un paciente"""
        existing_paciente = await self.paciente_repo.get_by_id(paciente_id)
        if not existing_paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        return await self.paciente_repo.delete(paciente_id)
    
    async def get_paciente_by_usuario(self, usuario_id: UUID) -> Optional[PacienteResponse]:
        """Obtener paciente por usuario_id"""
        paciente = await self.paciente_repo.get_by_usuario_id(usuario_id)
        if paciente:
            return PacienteResponse(**paciente)
        return None
    
    async def get_pacientes_by_seguro(self, seguro: str) -> List[PacienteResponse]:
        """Obtener pacientes por seguro médico"""
        pacientes = await self.paciente_repo.get_by_seguro_medico(seguro)
        return [PacienteResponse(**paciente) for paciente in pacientes]
    
    async def search_pacientes_by_name(self, nombre: str) -> List[PacienteResponse]:
        """Buscar pacientes por nombre"""
        pacientes = await self.paciente_repo.search_by_name(nombre)
        return [PacienteResponse(**paciente) for paciente in pacientes]
