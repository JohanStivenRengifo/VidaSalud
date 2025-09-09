"""
Endpoints para la gestión de consultorios
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from app.models.consultorio import Consultorio, ConsultorioCreate, ConsultorioUpdate, ConsultorioResponse
from app.services.consultorio_service import ConsultorioService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/consultorios", tags=["Consultorios"])

consultorio_service = ConsultorioService()


@router.post("/", response_model=ConsultorioResponse, status_code=status.HTTP_201_CREATED, summary="Crear consultorio")
async def create_consultorio(
    consultorio_data: ConsultorioCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear un nuevo consultorio
    
    - **nombre**: Nombre único del consultorio
    - **descripcion**: Descripción del consultorio (opcional)
    - **ubicacion**: Ubicación del consultorio (opcional)
    - **capacidad**: Capacidad del consultorio (por defecto 1, máximo 10)
    - **equipamiento**: Equipamiento disponible (opcional)
    - **activo**: Si el consultorio está activo (por defecto True)
    
    Requiere autenticación
    """
    return await consultorio_service.create_consultorio(consultorio_data)


@router.get("/", response_model=List[ConsultorioResponse], summary="Listar consultorios")
async def get_consultorios(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de consultorios con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await consultorio_service.get_consultorios(skip, limit)


@router.get("/activos", response_model=List[ConsultorioResponse], summary="Listar consultorios activos")
async def get_consultorios_activos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de consultorios activos con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await consultorio_service.get_consultorios_activos(skip, limit)


@router.get("/{consultorio_id}", response_model=ConsultorioResponse, summary="Obtener consultorio por ID")
async def get_consultorio(
    consultorio_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener un consultorio específico por su ID
    
    - **consultorio_id**: ID único del consultorio
    
    Requiere autenticación
    """
    return await consultorio_service.get_consultorio(consultorio_id)


@router.put("/{consultorio_id}", response_model=ConsultorioResponse, summary="Actualizar consultorio")
async def update_consultorio(
    consultorio_id: UUID,
    consultorio_data: ConsultorioUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de un consultorio
    
    - **consultorio_id**: ID único del consultorio
    - **consultorio_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await consultorio_service.update_consultorio(consultorio_id, consultorio_data)


@router.delete("/{consultorio_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar consultorio")
async def delete_consultorio(
    consultorio_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar un consultorio (soft delete - marca como inactivo)
    
    - **consultorio_id**: ID único del consultorio
    
    Requiere autenticación
    """
    await consultorio_service.delete_consultorio(consultorio_id)


@router.get("/ubicacion/{ubicacion}", response_model=List[ConsultorioResponse], summary="Obtener consultorios por ubicación")
async def get_consultorios_by_ubicacion(
    ubicacion: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener consultorios por ubicación
    
    - **ubicacion**: Ubicación a buscar (búsqueda parcial)
    
    Requiere autenticación
    """
    return await consultorio_service.get_consultorios_by_ubicacion(ubicacion)


@router.get("/capacidad/{capacidad_min}", response_model=List[ConsultorioResponse], summary="Obtener consultorios por capacidad")
async def get_consultorios_by_capacidad(
    capacidad_min: int = Path(..., ge=1, le=10, description="Capacidad mínima"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener consultorios con capacidad mínima
    
    - **capacidad_min**: Capacidad mínima requerida (1-10)
    
    Requiere autenticación
    """
    return await consultorio_service.get_consultorios_by_capacidad(capacidad_min)
