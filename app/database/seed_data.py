"""
Datos iniciales para la base de datos
"""
from app.database import db_connection
import logging

logger = logging.getLogger(__name__)


async def create_default_roles():
    """Crear roles por defecto"""
    try:
        client = db_connection.client
        
        # Verificar si ya existen roles
        result = client.table("roles").select("id").execute()
        if result.data:
            logger.info("Los roles ya existen, omitiendo creación")
            return
        
        # Crear roles por defecto
        roles = [
            {
                "nombre": "Administrador",
                "descripcion": "Administrador del sistema con acceso completo"
            },
            {
                "nombre": "Medico",
                "descripcion": "Médico que puede atender pacientes"
            },
            {
                "nombre": "Paciente",
                "descripcion": "Paciente que puede agendar citas"
            }
        ]
        
        for role in roles:
            client.table("roles").insert(role).execute()
        
        logger.info("Roles por defecto creados exitosamente")
        
    except Exception as e:
        logger.error(f"Error al crear roles por defecto: {e}")
        # No lanzar excepción, solo loggear el error
        logger.warning("Continuando sin crear roles por defecto")


async def create_default_estados_cita():
    """Crear estados de cita por defecto"""
    try:
        client = db_connection.client
        
        # Verificar si ya existen estados
        result = client.table("estados_cita").select("id").execute()
        if result.data:
            logger.info("Los estados de cita ya existen, omitiendo creación")
            return
        
        # Crear estados por defecto
        estados = [
            {
                "nombre": "Programada",
                "descripcion": "Cita programada y confirmada",
                "color": "#3B82F6"
            },
            {
                "nombre": "En Progreso",
                "descripcion": "Cita en curso",
                "color": "#F59E0B"
            },
            {
                "nombre": "Completada",
                "descripcion": "Cita completada exitosamente",
                "color": "#10B981"
            },
            {
                "nombre": "Cancelada",
                "descripcion": "Cita cancelada",
                "color": "#EF4444"
            },
            {
                "nombre": "No Asistió",
                "descripcion": "Paciente no asistió a la cita",
                "color": "#6B7280"
            }
        ]
        
        for estado in estados:
            client.table("estados_cita").insert(estado).execute()
        
        logger.info("Estados de cita por defecto creados exitosamente")
        
    except Exception as e:
        logger.error(f"Error al crear estados de cita por defecto: {e}")
        # No lanzar excepción, solo loggear el error
        logger.warning("Continuando sin crear estados de cita por defecto")


async def create_default_especialidades():
    """Crear especialidades médicas por defecto"""
    try:
        client = db_connection.client
        
        # Verificar si ya existen especialidades
        result = client.table("especialidades").select("id").execute()
        if result.data:
            logger.info("Las especialidades ya existen, omitiendo creación")
            return
        
        # Crear especialidades por defecto
        especialidades = [
            {
                "nombre": "Medicina General",
                "descripcion": "Atención médica general y preventiva",
                "duracion_cita_default": 30,
                "precio_base": 50000
            },
            {
                "nombre": "Cardiología",
                "descripcion": "Especialidad en enfermedades del corazón",
                "duracion_cita_default": 45,
                "precio_base": 80000
            },
            {
                "nombre": "Dermatología",
                "descripcion": "Especialidad en enfermedades de la piel",
                "duracion_cita_default": 30,
                "precio_base": 70000
            },
            {
                "nombre": "Pediatría",
                "descripcion": "Especialidad en medicina infantil",
                "duracion_cita_default": 30,
                "precio_base": 60000
            },
            {
                "nombre": "Ginecología",
                "descripcion": "Especialidad en salud reproductiva femenina",
                "duracion_cita_default": 45,
                "precio_base": 75000
            }
        ]
        
        for especialidad in especialidades:
            client.table("especialidades").insert(especialidad).execute()
        
        logger.info("Especialidades por defecto creadas exitosamente")
        
    except Exception as e:
        logger.error(f"Error al crear especialidades por defecto: {e}")
        # No lanzar excepción, solo loggear el error
        logger.warning("Continuando sin crear especialidades por defecto")


async def seed_database():
    """Ejecutar todos los datos iniciales"""
    try:
        logger.info("Iniciando carga de datos iniciales...")
        
        await create_default_roles()
        await create_default_estados_cita()
        await create_default_especialidades()
        
        logger.info("Datos iniciales cargados exitosamente")
        
    except Exception as e:
        logger.error(f"Error al cargar datos iniciales: {e}")
        # No lanzar excepción, solo loggear el error
        logger.warning("Continuando sin cargar datos iniciales")
