"""
Middleware para CORS
"""
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def setup_cors(app):
    """Configurar CORS para la aplicación"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )
