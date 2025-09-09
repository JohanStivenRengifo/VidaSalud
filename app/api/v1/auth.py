"""
Endpoints de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.usuario import UsuarioLogin, Token, UsuarioResponse
from app.services.auth_service import AuthService
from app.services.usuario_service import UsuarioService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])

auth_service = AuthService()
usuario_service = UsuarioService()


@router.post("/login", response_model=Token, summary="Iniciar sesión")
async def login(login_data: UsuarioLogin):
    """
    Iniciar sesión con email y contraseña
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT para autenticación
    """
    return await auth_service.login(login_data)


@router.post("/login-form", response_model=Token, summary="Iniciar sesión (formulario)")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Iniciar sesión usando formulario OAuth2
    
    - **username**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT para autenticación
    """
    login_data = UsuarioLogin(email=form_data.username, password=form_data.password)
    return await auth_service.login(login_data)


@router.get("/me", response_model=UsuarioResponse, summary="Obtener usuario actual")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtener información del usuario autenticado
    
    Requiere token JWT válido
    """
    return UsuarioResponse(**current_user)


@router.post("/verify-email/{usuario_id}", response_model=UsuarioResponse, summary="Verificar email")
async def verify_email(usuario_id: str):
    """
    Verificar email de un usuario
    
    - **usuario_id**: ID del usuario a verificar
    """
    from uuid import UUID
    return await usuario_service.verify_email(UUID(usuario_id))


@router.post("/refresh", response_model=Token, summary="Renovar token")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Renovar token de autenticación
    
    Requiere token JWT válido
    """
    from app.models.usuario import UsuarioLogin
    from datetime import timedelta
    from app.config import settings
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(current_user["id"])}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )
