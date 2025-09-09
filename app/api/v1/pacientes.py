"""
Endpoints para la gestión de pacientes
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.paciente import Paciente, PacienteCreate, PacienteUpdate, PacienteResponse
from app.services.paciente_service import PacienteService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

paciente_service = PacienteService()


@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED, summary="Crear paciente")
async def create_paciente(
    paciente_data: PacienteCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear un nuevo paciente
    
    - **usuario_id**: ID del usuario asociado
    - **tipo_sangre**: Tipo de sangre (opcional)
    - **alergias**: Alergias del paciente (opcional)
    - **enfermedades_cronicas**: Enfermedades crónicas (opcional)
    - **medicamentos_actuales**: Medicamentos actuales (opcional)
    - **contacto_emergencia_nombre**: Nombre del contacto de emergencia (opcional)
    - **contacto_emergencia_telefono**: Teléfono del contacto de emergencia (opcional)
    - **seguro_medico**: Seguro médico (opcional)
    - **numero_seguro**: Número de seguro (opcional)
    
    Requiere autenticación
    """
    return await paciente_service.create_paciente(paciente_data)


@router.get("/", response_model=List[PacienteResponse], summary="Listar pacientes")
async def get_pacientes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de pacientes con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await paciente_service.get_pacientes(skip, limit)


@router.get("/{paciente_id}", response_model=PacienteResponse, summary="Obtener paciente por ID")
async def get_paciente(
    paciente_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener un paciente específico por su ID
    
    - **paciente_id**: ID único del paciente
    
    Requiere autenticación
    """
    return await paciente_service.get_paciente(paciente_id)


@router.put("/{paciente_id}", response_model=PacienteResponse, summary="Actualizar paciente")
async def update_paciente(
    paciente_id: UUID,
    paciente_data: PacienteUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de un paciente
    
    - **paciente_id**: ID único del paciente
    - **paciente_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await paciente_service.update_paciente(paciente_id, paciente_data)


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar paciente")
async def delete_paciente(
    paciente_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar un paciente
    
    - **paciente_id**: ID único del paciente
    
    Requiere autenticación
    """
    await paciente_service.delete_paciente(paciente_id)


@router.get("/usuario/{usuario_id}", response_model=PacienteResponse, summary="Obtener paciente por usuario")
async def get_paciente_by_usuario(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener paciente por ID de usuario
    
    - **usuario_id**: ID del usuario
    
    Requiere autenticación
    """
    paciente = await paciente_service.get_paciente_by_usuario(usuario_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    return paciente


@router.get("/seguro/{seguro}", response_model=List[PacienteResponse], summary="Obtener pacientes por seguro")
async def get_pacientes_by_seguro(
    seguro: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener pacientes por seguro médico
    
    - **seguro**: Nombre del seguro médico
    
    Requiere autenticación
    """
    return await paciente_service.get_pacientes_by_seguro(seguro)


@router.get("/buscar/{nombre}", response_model=List[PacienteResponse], summary="Buscar pacientes por nombre")
async def search_pacientes_by_name(
    nombre: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Buscar pacientes por nombre
    
    - **nombre**: Nombre a buscar (búsqueda parcial)
    
    Requiere autenticación
    """
    return await paciente_service.search_pacientes_by_name(nombre)
