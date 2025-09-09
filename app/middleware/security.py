"""
Middleware de seguridad
"""
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.config import settings


def setup_security(app: FastAPI):
    """Configurar middleware de seguridad"""
    
    # Solo en producción, redirigir HTTP a HTTPS
    if settings.environment == "production":
        app.add_middleware(HTTPSRedirectMiddleware)
    
    # Configurar hosts confiables
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
    )
