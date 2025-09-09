"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_role_key: str
    
    # Configuración de JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de la aplicación
    debug: bool = False
    environment: str = "development"
    app_name: str = "Sistema de Reservas Médicas"
    version: str = "1.0.0"
    
    # Configuración de CORS
    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
