"""
Endpoints para la gestión de calificaciones
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.calificacion import Calificacion, CalificacionCreate, CalificacionUpdate, CalificacionResponse, CalificacionConDetalles
from app.services.calificacion_service import CalificacionService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])

calificacion_service = CalificacionService()


@router.post("/", response_model=CalificacionResponse, status_code=status.HTTP_201_CREATED, summary="Crear calificación")
async def create_calificacion(
    calificacion_data: CalificacionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva calificación
    
    - **cita_id**: ID de la cita a calificar
    - **paciente_id**: ID del paciente que califica
    - **medico_id**: ID del médico calificado
    - **calificacion**: Calificación del 1 al 5
    - **comentario**: Comentario sobre la calificación (opcional)
    
    Requiere autenticación
    """
    return await calificacion_service.create_calificacion(calificacion_data)


@router.get("/", response_model=List[CalificacionResponse], summary="Listar calificaciones")
async def get_calificaciones(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de calificaciones con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await calificacion_service.get_calificaciones(skip, limit)


@router.get("/detalles", response_model=List[CalificacionConDetalles], summary="Listar calificaciones con detalles")
async def get_calificaciones_with_details(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de calificaciones con información detallada (paciente, médico, cita)
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await calificacion_service.get_calificaciones_with_details(skip, limit)


@router.get("/{calificacion_id}", response_model=CalificacionResponse, summary="Obtener calificación por ID")
async def get_calificacion(
    calificacion_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener una calificación específica por su ID
    
    - **calificacion_id**: ID único de la calificación
    
    Requiere autenticación
    """
    return await calificacion_service.get_calificacion(calificacion_id)


@router.put("/{calificacion_id}", response_model=CalificacionResponse, summary="Actualizar calificación")
async def update_calificacion(
    calificacion_id: UUID,
    calificacion_data: CalificacionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de una calificación
    
    - **calificacion_id**: ID único de la calificación
    - **calificacion_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await calificacion_service.update_calificacion(calificacion_id, calificacion_data)


@router.delete("/{calificacion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar calificación")
async def delete_calificacion(
    calificacion_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar una calificación
    
    - **calificacion_id**: ID único de la calificación
    
    Requiere autenticación
    """
    await calificacion_service.delete_calificacion(calificacion_id)


@router.get("/paciente/{paciente_id}", response_model=List[CalificacionResponse], summary="Obtener calificaciones por paciente")
async def get_calificaciones_by_paciente(
    paciente_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener calificaciones realizadas por un paciente
    
    - **paciente_id**: ID del paciente
    
    Requiere autenticación
    """
    return await calificacion_service.get_calificaciones_by_paciente(paciente_id)


@router.get("/medico/{medico_id}", response_model=List[CalificacionResponse], summary="Obtener calificaciones por médico")
async def get_calificaciones_by_medico(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener calificaciones recibidas por un médico
    
    - **medico_id**: ID del médico
    
    Requiere autenticación
    """
    return await calificacion_service.get_calificaciones_by_medico(medico_id)


@router.get("/cita/{cita_id}", response_model=CalificacionResponse, summary="Obtener calificación por cita")
async def get_calificacion_by_cita(
    cita_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener calificación de una cita específica
    
    - **cita_id**: ID de la cita
    
    Requiere autenticación
    """
    calificacion = await calificacion_service.get_calificacion_by_cita(cita_id)
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe calificación para esta cita"
        )
    return calificacion


@router.get("/medico/{medico_id}/promedio", response_model=dict, summary="Obtener calificación promedio de médico")
async def get_promedio_medico(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener calificación promedio de un médico
    
    - **medico_id**: ID del médico
    
    Retorna un objeto con la calificación promedio
    
    Requiere autenticación
    """
    promedio = await calificacion_service.get_promedio_medico(medico_id)
    return {"medico_id": str(medico_id), "calificacion_promedio": promedio}
