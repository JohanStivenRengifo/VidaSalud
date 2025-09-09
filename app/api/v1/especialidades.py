"""
Endpoints para la gestión de especialidades médicas
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.especialidad import Especialidad, EspecialidadCreate, EspecialidadUpdate, EspecialidadResponse
from app.services.especialidad_service import EspecialidadService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])

especialidad_service = EspecialidadService()


@router.post("/", response_model=EspecialidadResponse, status_code=status.HTTP_201_CREATED, summary="Crear especialidad")
async def create_especialidad(
    especialidad_data: EspecialidadCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva especialidad médica
    
    - **nombre**: Nombre único de la especialidad
    - **descripcion**: Descripción de la especialidad (opcional)
    - **duracion_cita_default**: Duración por defecto de las citas en minutos (por defecto 30)
    - **precio_base**: Precio base de la especialidad (opcional)
    - **activo**: Si la especialidad está activa (por defecto True)
    
    Requiere autenticación
    """
    return await especialidad_service.create_especialidad(especialidad_data)


@router.get("/", response_model=List[EspecialidadResponse], summary="Listar especialidades")
async def get_especialidades(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de especialidades con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await especialidad_service.get_especialidades(skip, limit)


@router.get("/activas", response_model=List[EspecialidadResponse], summary="Listar especialidades activas")
async def get_especialidades_activas(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de especialidades activas con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await especialidad_service.get_especialidades_activas(skip, limit)


@router.get("/{especialidad_id}", response_model=EspecialidadResponse, summary="Obtener especialidad por ID")
async def get_especialidad(
    especialidad_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener una especialidad específica por su ID
    
    - **especialidad_id**: ID único de la especialidad
    
    Requiere autenticación
    """
    return await especialidad_service.get_especialidad(especialidad_id)


@router.put("/{especialidad_id}", response_model=EspecialidadResponse, summary="Actualizar especialidad")
async def update_especialidad(
    especialidad_id: UUID,
    especialidad_data: EspecialidadUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de una especialidad
    
    - **especialidad_id**: ID único de la especialidad
    - **especialidad_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await especialidad_service.update_especialidad(especialidad_id, especialidad_data)


@router.delete("/{especialidad_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar especialidad")
async def delete_especialidad(
    especialidad_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar una especialidad (soft delete - marca como inactiva)
    
    - **especialidad_id**: ID único de la especialidad
    
    Requiere autenticación
    """
    await especialidad_service.delete_especialidad(especialidad_id)


@router.get("/buscar/{nombre}", response_model=List[EspecialidadResponse], summary="Buscar especialidades por nombre")
async def search_especialidades(
    nombre: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Buscar especialidades por nombre
    
    - **nombre**: Nombre a buscar (búsqueda parcial)
    
    Requiere autenticación
    """
    return await especialidad_service.search_especialidades(nombre)
