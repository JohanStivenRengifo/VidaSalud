"""
Endpoints para la gestión de médicos
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from app.models.medico import Medico, MedicoCreate, MedicoUpdate, MedicoResponse, MedicoConEspecialidad
from app.services.medico_service import MedicoService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/medicos", tags=["Médicos"])

medico_service = MedicoService()


@router.post("/", response_model=MedicoResponse, status_code=status.HTTP_201_CREATED, summary="Crear médico")
async def create_medico(
    medico_data: MedicoCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear un nuevo médico
    
    - **usuario_id**: ID del usuario asociado
    - **especialidad_id**: ID de la especialidad
    - **numero_licencia**: Número de licencia médica (único)
    - **universidad**: Universidad donde estudió (opcional)
    - **anos_experiencia**: Años de experiencia (opcional)
    - **biografia**: Biografía del médico (opcional)
    - **precio_consulta**: Precio de la consulta (opcional)
    - **disponible**: Si está disponible para citas (por defecto True)
    
    Requiere autenticación
    """
    return await medico_service.create_medico(medico_data)


@router.get("/", response_model=List[MedicoResponse], summary="Listar médicos")
async def get_medicos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de médicos con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await medico_service.get_medicos(skip, limit)


@router.get("/detalles", response_model=List[MedicoConEspecialidad], summary="Listar médicos con especialidad")
async def get_medicos_with_especialidad(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de médicos con información de especialidad
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await medico_service.get_medicos_with_especialidad(skip, limit)


@router.get("/{medico_id}", response_model=MedicoResponse, summary="Obtener médico por ID")
async def get_medico(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener un médico específico por su ID
    
    - **medico_id**: ID único del médico
    
    Requiere autenticación
    """
    return await medico_service.get_medico(medico_id)


@router.put("/{medico_id}", response_model=MedicoResponse, summary="Actualizar médico")
async def update_medico(
    medico_id: UUID,
    medico_data: MedicoUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de un médico
    
    - **medico_id**: ID único del médico
    - **medico_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await medico_service.update_medico(medico_id, medico_data)


@router.delete("/{medico_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar médico")
async def delete_medico(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar un médico (soft delete - marca como no disponible)
    
    - **medico_id**: ID único del médico
    
    Requiere autenticación
    """
    await medico_service.delete_medico(medico_id)


@router.get("/usuario/{usuario_id}", response_model=MedicoResponse, summary="Obtener médico por usuario")
async def get_medico_by_usuario(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener médico por ID de usuario
    
    - **usuario_id**: ID del usuario
    
    Requiere autenticación
    """
    medico = await medico_service.get_medico_by_usuario(usuario_id)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico no encontrado"
        )
    return medico


@router.get("/especialidad/{especialidad_id}", response_model=List[MedicoResponse], summary="Obtener médicos por especialidad")
async def get_medicos_by_especialidad(
    especialidad_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener médicos por especialidad
    
    - **especialidad_id**: ID de la especialidad
    
    Requiere autenticación
    """
    return await medico_service.get_medicos_by_especialidad(especialidad_id)


@router.get("/disponibles", response_model=List[MedicoResponse], summary="Obtener médicos disponibles")
async def get_medicos_disponibles(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener médicos disponibles para citas
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await medico_service.get_medicos_disponibles(skip, limit)


@router.get("/calificacion/{calificacion_min}", response_model=List[MedicoResponse], summary="Obtener médicos por calificación")
async def get_medicos_by_calificacion(
    calificacion_min: float = Path(..., ge=0, le=5, description="Calificación mínima"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener médicos con calificación mínima
    
    - **calificacion_min**: Calificación mínima (0-5)
    
    Requiere autenticación
    """
    return await medico_service.get_medicos_by_calificacion(calificacion_min)


@router.post("/{medico_id}/actualizar-calificacion", response_model=MedicoResponse, summary="Actualizar calificación promedio")
async def update_calificacion_promedio(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar calificación promedio de un médico basada en sus calificaciones
    
    - **medico_id**: ID del médico
    
    Requiere autenticación
    """
    return await medico_service.update_calificacion_promedio(medico_id)
