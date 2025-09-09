"""
Configuración de conexión a Supabase
"""
from supabase import create_client, Client
from app.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Singleton para manejar la conexión a Supabase"""
    
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _connect(self) -> None:
        """Establece la conexión con Supabase"""
        try:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
            logger.info("Conexión a Supabase establecida correctamente")
        except Exception as e:
            logger.error(f"Error al conectar con Supabase: {e}")
            raise
    
    @property
    def client(self) -> Client:
        """Retorna el cliente de Supabase"""
        if self._client is None:
            self._connect()
        return self._client
    
    def get_service_client(self) -> Client:
        """Retorna el cliente de Supabase con service role key"""
        try:
            return create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        except Exception as e:
            logger.error(f"Error al crear cliente de servicio: {e}")
            raise


# Instancia global de la conexión
db_connection = DatabaseConnection()
