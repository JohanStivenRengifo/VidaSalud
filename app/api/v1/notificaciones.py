"""
Endpoints para la gestión de notificaciones
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.models.notificacion import Notificacion, NotificacionCreate, NotificacionUpdate, NotificacionResponse
from app.services.notificacion_service import NotificacionService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

notificacion_service = NotificacionService()


@router.post("/", response_model=NotificacionResponse, status_code=status.HTTP_201_CREATED, summary="Crear notificación")
async def create_notificacion(
    notificacion_data: NotificacionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva notificación
    
    - **usuario_id**: ID del usuario destinatario
    - **titulo**: Título de la notificación
    - **mensaje**: Mensaje de la notificación
    - **tipo**: Tipo de notificación (info, warning, error, success)
    - **cita_id**: ID de la cita relacionada (opcional)
    
    Requiere autenticación
    """
    return await notificacion_service.create_notificacion(notificacion_data)


@router.get("/", response_model=List[NotificacionResponse], summary="Listar notificaciones")
async def get_notificaciones(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de notificaciones con paginación
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    
    Requiere autenticación
    """
    return await notificacion_service.get_notificaciones(skip, limit)


@router.get("/{notificacion_id}", response_model=NotificacionResponse, summary="Obtener notificación por ID")
async def get_notificacion(
    notificacion_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener una notificación específica por su ID
    
    - **notificacion_id**: ID único de la notificación
    
    Requiere autenticación
    """
    return await notificacion_service.get_notificacion(notificacion_id)


@router.put("/{notificacion_id}", response_model=NotificacionResponse, summary="Actualizar notificación")
async def update_notificacion(
    notificacion_id: UUID,
    notificacion_data: NotificacionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de una notificación
    
    - **notificacion_id**: ID único de la notificación
    - **notificacion_data**: Datos a actualizar (todos los campos son opcionales)
    
    Requiere autenticación
    """
    return await notificacion_service.update_notificacion(notificacion_id, notificacion_data)


@router.delete("/{notificacion_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar notificación")
async def delete_notificacion(
    notificacion_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Eliminar una notificación
    
    - **notificacion_id**: ID único de la notificación
    
    Requiere autenticación
    """
    await notificacion_service.delete_notificacion(notificacion_id)


@router.get("/usuario/{usuario_id}", response_model=List[NotificacionResponse], summary="Obtener notificaciones por usuario")
async def get_notificaciones_by_usuario(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener notificaciones de un usuario específico
    
    - **usuario_id**: ID del usuario
    
    Requiere autenticación
    """
    return await notificacion_service.get_notificaciones_by_usuario(usuario_id)


@router.get("/usuario/{usuario_id}/no-leidas", response_model=List[NotificacionResponse], summary="Obtener notificaciones no leídas")
async def get_notificaciones_no_leidas(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener notificaciones no leídas de un usuario
    
    - **usuario_id**: ID del usuario
    
    Requiere autenticación
    """
    return await notificacion_service.get_notificaciones_no_leidas(usuario_id)


@router.get("/usuario/{usuario_id}/tipo/{tipo}", response_model=List[NotificacionResponse], summary="Obtener notificaciones por tipo")
async def get_notificaciones_by_tipo(
    usuario_id: UUID,
    tipo: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener notificaciones de un usuario por tipo
    
    - **usuario_id**: ID del usuario
    - **tipo**: Tipo de notificación (info, warning, error, success)
    
    Requiere autenticación
    """
    return await notificacion_service.get_notificaciones_by_tipo(usuario_id, tipo)


@router.post("/{notificacion_id}/leer", response_model=NotificacionResponse, summary="Marcar notificación como leída")
async def marcar_como_leida(
    notificacion_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Marcar una notificación como leída
    
    - **notificacion_id**: ID de la notificación
    
    Requiere autenticación
    """
    return await notificacion_service.marcar_como_leida(notificacion_id)


@router.post("/usuario/{usuario_id}/leer-todas", status_code=status.HTTP_204_NO_CONTENT, summary="Marcar todas las notificaciones como leídas")
async def marcar_todas_como_leidas(
    usuario_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """
    Marcar todas las notificaciones de un usuario como leídas
    
    - **usuario_id**: ID del usuario
    
    Requiere autenticación
    """
    await notificacion_service.marcar_todas_como_leidas(usuario_id)


@router.post("/cita", response_model=NotificacionResponse, summary="Crear notificación de cita")
async def create_notificacion_cita(
    usuario_id: UUID,
    cita_id: UUID,
    titulo: str,
    mensaje: str,
    tipo: str = "info",
    current_user: dict = Depends(get_current_user)
):
    """
    Crear notificación relacionada con una cita
    
    - **usuario_id**: ID del usuario destinatario
    - **cita_id**: ID de la cita
    - **titulo**: Título de la notificación
    - **mensaje**: Mensaje de la notificación
    - **tipo**: Tipo de notificación (por defecto "info")
    
    Requiere autenticación
    """
    return await notificacion_service.create_notificacion_cita(usuario_id, cita_id, titulo, mensaje, tipo)


@router.post("/general", response_model=NotificacionResponse, summary="Crear notificación general")
async def create_notificacion_general(
    usuario_id: UUID,
    titulo: str,
    mensaje: str,
    tipo: str = "info",
    current_user: dict = Depends(get_current_user)
):
    """
    Crear notificación general
    
    - **usuario_id**: ID del usuario destinatario
    - **titulo**: Título de la notificación
    - **mensaje**: Mensaje de la notificación
    - **tipo**: Tipo de notificación (por defecto "info")
    
    Requiere autenticación
    """
    return await notificacion_service.create_notificacion_general(usuario_id, titulo, mensaje, tipo)
