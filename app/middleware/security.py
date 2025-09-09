"""
Middleware de seguridad
"""
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.config import settings


def setup_security(app: FastAPI):
    """Configurar middleware de seguridad"""
    
    # No redirigir HTTP a HTTPS en Railway para evitar problemas con healthcheck
    # if settings.environment == "production":
    #     app.add_middleware(HTTPSRedirectMiddleware)
    
    # Configurar hosts confiables - temporalmente permitir todos para Railway
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]
    )
