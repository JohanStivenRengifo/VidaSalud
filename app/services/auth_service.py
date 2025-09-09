"""
Servicio de autenticación integrado con Supabase Auth
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from supabase import Client

from app.config import settings
from app.models.usuario import UsuarioLogin, Token
from app.database import db_connection


class AuthService:
    """Servicio para manejo de autenticación con Supabase Auth"""
    
    def __init__(self):
        # Usar cliente normal para autenticación
        self.client = db_connection.client
    
    async def login(self, login_data: UsuarioLogin) -> Token:
        """Iniciar sesión usando Supabase Auth"""
        try:
            # Autenticar con Supabase Auth
            response = self.client.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Obtener información del perfil del usuario
            user_profile = await self._get_user_profile(response.user.id)
            
            if not user_profile or not user_profile.get("activo", True):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario inactivo"
                )
            
            return Token(
                access_token=response.session.access_token,
                token_type="bearer",
                expires_in=response.session.expires_in
            )
            
        except Exception as e:
            if "Invalid login credentials" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error en autenticación: {str(e)}"
                )
    
    async def _get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener perfil del usuario desde la tabla usuarios"""
        try:
            result = self.client.table("usuarios").select("*").eq("id", user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception:
            return None
    
    async def get_current_user(self, token: str) -> Dict[str, Any]:
        """Obtener usuario actual desde token de Supabase"""
        try:
            # Verificar token con Supabase
            response = self.client.auth.get_user(token)
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Obtener perfil completo
            user_profile = await self._get_user_profile(response.user.id)
            if not user_profile:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Perfil de usuario no encontrado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user_profile
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def register(self, email: str, password: str, user_data: Dict[str, Any]) -> Token:
        """Registrar nuevo usuario"""
        try:
            # Crear usuario en Supabase Auth
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "nombre": user_data.get("nombre"),
                        "apellidos": user_data.get("apellidos")
                    }
                }
            })
            
            if not response.user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error al crear usuario"
                )
            
            # Crear perfil en tabla usuarios
            profile_data = {
                "id": response.user.id,
                "email": email,
                "nombre": user_data.get("nombre"),
                "apellidos": user_data.get("apellidos"),
                "telefono": user_data.get("telefono"),
                "fecha_nacimiento": user_data.get("fecha_nacimiento"),
                "genero": user_data.get("genero"),
                "direccion": user_data.get("direccion"),
                "documento_identidad": user_data.get("documento_identidad"),
                "tipo_documento": user_data.get("tipo_documento"),
                "rol_id": user_data.get("rol_id"),
                "activo": True,
                "email_verificado": False
            }
            
            self.client.table("usuarios").insert(profile_data).execute()
            
            return Token(
                access_token=response.session.access_token if response.session else "",
                token_type="bearer",
                expires_in=response.session.expires_in if response.session else 3600
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al registrar usuario: {str(e)}"
            )
    
    async def logout(self, token: str) -> bool:
        """Cerrar sesión"""
        try:
            self.client.auth.sign_out()
            return True
        except Exception:
            return False
    
    async def verify_token(self, token: str) -> bool:
        """Verificar si un token es válido"""
        try:
            response = self.client.auth.get_user(token)
            return response.user is not None
        except Exception:
            return False
