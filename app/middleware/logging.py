"""
Middleware para logging
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests"""
    
    async def dispatch(self, request: Request, call_next):
        # Log del request
        start_time = time.time()
        
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Procesar request
        response = await call_next(request)
        
        # Log del response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
        
        return response
