"""
Aplicación principal de FastAPI para el Sistema de Reservas Médicas
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.api.v1.router import api_router
from app.middleware.cors import setup_cors
from app.middleware.security import setup_security
from app.middleware.logging import LoggingMiddleware
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando Sistema de Reservas Médicas...")
    logger.info(f"Entorno: {settings.environment}")
    logger.info(f"Debug: {settings.debug}")
    
    # Verificar conexión a Supabase
    try:
        from app.database import db_connection
        # Test de conexión
        client = db_connection.client
        logger.info("Conexión a Supabase establecida correctamente")
        
        # Cargar datos iniciales
        from app.database.seed_data import seed_database
        await seed_database()
        
    except Exception as e:
        logger.error(f"Error al conectar con Supabase: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Cerrando Sistema de Reservas Médicas...")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Sistema de Reservas para Consultorios Médicos
    
    API REST desarrollada con FastAPI para la gestión de reservas médicas.
    
    ### Características principales:
    - **Gestión de usuarios**: Registro y autenticación de usuarios
    - **Gestión de pacientes**: Información médica y datos personales
    - **Gestión de médicos**: Especialidades, horarios y disponibilidad
    - **Gestión de citas**: Reservas, cancelaciones y seguimiento
    - **Calificaciones**: Sistema de calificaciones para médicos
    - **Notificaciones**: Sistema de notificaciones en tiempo real
    - **Consultorios**: Gestión de espacios físicos
    
    ### Autenticación:
    La API utiliza JWT (JSON Web Tokens) para la autenticación. 
    Incluye el token en el header `Authorization: Bearer <token>`
    
    ### Documentación:
    - **Swagger UI**: `/docs` - Interfaz interactiva para probar la API
    - **ReDoc**: `/redoc` - Documentación alternativa
    """,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configurar middleware
setup_cors(app)
setup_security(app)
app.add_middleware(LoggingMiddleware)

# Configurar manejadores de errores
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Incluir routers
app.include_router(api_router)


@app.get("/", tags=["Root"], summary="Información de la API")
async def root():
    """
    Endpoint raíz con información básica de la API
    """
    return {
        "message": "Bienvenido al Sistema de Reservas Médicas",
        "version": settings.version,
        "environment": settings.environment,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_url": "/api/v1"
    }


@app.get("/health", tags=["Health"], summary="Estado de la aplicación")
async def health_check():
    """
    Endpoint de salud para verificar el estado de la aplicación
    """
    try:
        from app.database import db_connection
        # Test de conexión a la base de datos
        client = db_connection.client
        # Aquí podrías hacer una consulta simple para verificar la conexión
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.version,
            "environment": settings.environment
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Obtener el puerto de Railway o usar 8000 por defecto
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level="info"
    )
