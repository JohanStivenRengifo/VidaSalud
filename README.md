# 🏥 Sistema de Reservas Médicas

API REST desarrollada con **FastAPI** para la gestión integral de reservas médicas, con arquitectura modular y patrones de diseño implementados.

## 🏗️ Arquitectura del Proyecto

```
app/
├── api/v1/           # Endpoints REST organizados por módulos
├── config/           # Configuración y variables de entorno
├── database/         # Conexión a Supabase y datos iniciales
├── middleware/       # CORS, seguridad, logging y manejo de errores
├── models/           # Modelos Pydantic para validación
├── repositories/     # Capa de acceso a datos (Repository Pattern)
├── services/         # Lógica de negocio (Service Layer)
└── main.py          # Aplicación principal FastAPI
```

## 📊 Modelo de Datos

### Entidades Principales

| Entidad          | Descripción                                            |
| ---------------- | ------------------------------------------------------ |
| **Usuario**      | Entidad base para médicos, pacientes y administradores |
| **Médico**       | Profesional médico con especialidad y horarios         |
| **Paciente**     | Usuario que puede agendar citas                        |
| **Cita**         | Reserva médica entre paciente y médico                 |
| **Especialidad** | Área médica (Cardiología, Dermatología, etc.)          |
| **Consultorio**  | Espacio físico para consultas                          |
| **Calificación** | Evaluación del paciente hacia el médico                |
| **Notificación** | Mensajes del sistema                                   |

### Relaciones Clave

- **Usuario** → **Médico/Paciente** (1:0..1)
- **Médico** → **Especialidad** (N:1)
- **Paciente** → **Cita** (1:N)
- **Médico** → **Cita** (1:N)
- **Cita** → **Calificación** (1:0..1)

## 🎯 Endpoints Principales

### Autenticación

- `POST /api/v1/auth/login` - Iniciar sesión
- `GET /api/v1/auth/me` - Obtener usuario actual
- `POST /api/v1/auth/refresh` - Renovar token

### Citas

- `GET /api/v1/citas/` - Listar citas
- `POST /api/v1/citas/` - Crear cita
- `GET /api/v1/citas/{id}` - Obtener cita específica
- `PUT /api/v1/citas/{id}` - Actualizar cita
- `GET /api/v1/citas/medico/{id}/horarios/{fecha}` - Horarios disponibles

### Médicos

- `GET /api/v1/medicos/` - Listar médicos
- `GET /api/v1/medicos/disponibles` - Médicos disponibles
- `GET /api/v1/medicos/especialidad/{id}` - Médicos por especialidad

### Especialidades

- `GET /api/v1/especialidades/` - Listar especialidades
- `GET /api/v1/especialidades/activas` - Especialidades activas

## 🧪 Testing

Ejecutar pruebas de endpoints:

```bash
python test_all_endpoints.py
```

## 🏛️ Patrones de Diseño Implementados

- **Repository Pattern** - Separación de acceso a datos
- **Service Layer** - Lógica de negocio centralizada
- **Factory Method** - Creación de objetos
- **Singleton** - Conexión a base de datos
- **Dependency Injection** - Inyección de dependencias con FastAPI

## 🔒 Seguridad

- **JWT Authentication** con Supabase Auth
- **CORS** configurado para desarrollo y producción
- **Validación de datos** con Pydantic
- **Middleware de seguridad** (HTTPS redirect, trusted hosts)
- **Manejo de errores** centralizado
- **Logging** estructurado

## 📈 Características Avanzadas

- **Paginación** en todos los endpoints de listado
- **Filtros y búsquedas** por múltiples criterios
- **Validación de horarios** para evitar conflictos
- **Sistema de calificaciones** con promedio automático
- **Notificaciones** para eventos importantes
- **Datos iniciales** (seed data) automáticos
