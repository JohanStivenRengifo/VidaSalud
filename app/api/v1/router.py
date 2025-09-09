"""
Router principal de la API v1
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .usuarios import router as usuarios_router
from .pacientes import router as pacientes_router
from .medicos import router as medicos_router
from .citas import router as citas_router
from .especialidades import router as especialidades_router
from .consultorios import router as consultorios_router
from .calificaciones import router as calificaciones_router
from .notificaciones import router as notificaciones_router

# Router principal de la API v1
api_router = APIRouter(prefix="/api/v1")

# Incluir todos los routers
api_router.include_router(auth_router)
api_router.include_router(usuarios_router)
api_router.include_router(pacientes_router)
api_router.include_router(medicos_router)
api_router.include_router(citas_router)
api_router.include_router(especialidades_router)
api_router.include_router(consultorios_router)
api_router.include_router(calificaciones_router)
api_router.include_router(notificaciones_router)
