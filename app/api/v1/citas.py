"""
Endpoints para la gestión de citas médicas
"""
from typing import List
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.cita import Cita, CitaCreate, CitaUpdate, CitaResponse, CitaConDetalles
from app.services.cita_service import CitaService
from app.api.dependencies import get_current_user, get_current_paciente, get_current_medico

router = APIRouter(prefix="/citas", tags=["Citas"])

cita_service = CitaService()


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED, summary="Crear cita")
async def create_cita(
    cita_data: CitaCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva cita médica
    
    - **paciente_id**: ID del paciente
    - **medico_id**: ID del médico
    - **consultorio_id**: ID del consultorio (opcional)
    - **fecha**: Fecha de la cita (no puede ser anterior a hoy)
    - **hora_inicio**: Hora de inicio de la cita
    - **hora_fin**: Hora de fin de la cita (debe ser posterior a hora_inicio)
    - **estado_id**: ID del estado de la cita
    - **motivo_consulta**: Motivo de la consulta (opcional)
    - **precio**: Precio de la consulta (opcional)
    
    Requiere autenticación
    """
    return await cita_service.create_cita(cita_data)


@router.get("/", response_model=List[CitaResponse], summary="Listar citas")
async def get_citas(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de citas con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await cita_service.get_citas(skip, limit)


@router.get("/detalles", response_model=List[CitaConDetalles], summary="Listar citas con detalles")
async def get_citas_with_details(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de citas con información detallada (paciente, médico, especialidad, etc.)
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await cita_service.get_citas_with_details(skip, limit)


@router.get("/pendientes-pago", response_model=List[CitaResponse], summary="Obtener citas pendientes de pago")
async def get_citas_pendientes_pago(
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener citas pendientes de pago
    
    Requiere autenticación
    """
    return await cita_service.get_citas_pendientes_pago()


@router.get("/{cita_id}", response_model=CitaResponse, summary="Obtener cita por ID")
async def get_cita(
    cita_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener una cita específica por su ID
    
    - **cita_id**: ID único de la cita
    
    Requiere autenticación
    """
    return await cita_service.get_cita(cita_id)


@router.put("/{cita_id}", response_model=CitaResponse, summary="Actualizar cita")
async def update_cita(
    cita_id: UUID,
    cita_data: CitaUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de una cita
    
    - **cita_id**: ID único de la cita
    - **cita_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await cita_service.update_cita(cita_id, cita_data)


@router.delete("/{cita_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar cita")
async def delete_cita(
    cita_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar una cita
    
    - **cita_id**: ID único de la cita
    
    Requiere autenticación
    """
    await cita_service.delete_cita(cita_id)


@router.get("/paciente/{paciente_id}", response_model=List[CitaConDetalles], summary="Obtener citas por paciente")
async def get_citas_by_paciente(
    paciente_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener citas de un paciente específico
    
    - **paciente_id**: ID del paciente
    
    Requiere autenticación
    """
    return await cita_service.get_citas_by_paciente(paciente_id)


@router.get("/medico/{medico_id}", response_model=List[CitaConDetalles], summary="Obtener citas por médico")
async def get_citas_by_medico(
    medico_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener citas de un médico específico
    
    - **medico_id**: ID del médico
    
    Requiere autenticación
    """
    return await cita_service.get_citas_by_medico(medico_id)


@router.get("/fecha/{fecha}", response_model=List[CitaResponse], summary="Obtener citas por fecha")
async def get_citas_by_fecha(
    fecha: date,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener citas de una fecha específica
    
    - **fecha**: Fecha en formato YYYY-MM-DD
    
    Requiere autenticación
    """
    return await cita_service.get_citas_by_fecha(fecha)


@router.get("/rango/{fecha_inicio}/{fecha_fin}", response_model=List[CitaResponse], summary="Obtener citas por rango de fechas")
async def get_citas_by_fecha_range(
    fecha_inicio: date,
    fecha_fin: date,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener citas en un rango de fechas
    
    - **fecha_inicio**: Fecha de inicio en formato YYYY-MM-DD
    - **fecha_fin**: Fecha de fin en formato YYYY-MM-DD
    
    Requiere autenticación
    """
    return await cita_service.get_citas_by_fecha_range(fecha_inicio, fecha_fin)


@router.post("/{cita_id}/pagar", response_model=CitaResponse, summary="Marcar cita como pagada")
async def marcar_cita_como_pagada(
    cita_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Marcar una cita como pagada
    
    - **cita_id**: ID único de la cita
    
    Requiere autenticación
    """
    return await cita_service.marcar_como_pagada(cita_id)


@router.get("/medico/{medico_id}/horarios/{fecha}", response_model=List[dict], summary="Obtener horarios disponibles")
async def get_horarios_disponibles(
    medico_id: UUID,
    fecha: date,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener horarios disponibles para un médico en una fecha específica
    
    - **medico_id**: ID del médico
    - **fecha**: Fecha en formato YYYY-MM-DD
    
    Retorna una lista de horarios disponibles con formato:
    - hora_inicio: Hora de inicio en formato HH:MM:SS
    - hora_fin: Hora de fin en formato HH:MM:SS
    
    Requiere autenticación
    """
    return await cita_service.get_horarios_disponibles(medico_id, fecha)
