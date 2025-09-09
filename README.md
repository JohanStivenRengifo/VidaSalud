# 🏥 Sistema de Reservas Médicas - API REST

### Estructura Modular

```

app/
├── config/          # Configuración y variables de entorno
├── database/        # Conexión y seed data
├── models/          # Modelos Pydantic
├── repositories/    # Capa de acceso a datos
├── services/        # Lógica de negocio
├── api/            # Endpoints REST
└── middleware/     # Middleware personalizado
```
# Modelo Relacional - Sistema de Gestión Médica

### Claves Primarias (PK):

- Todas las tablas tienen un campo `id` de tipo UUID como clave primaria

### Claves Foráneas (FK):

- `usuario.rol_id` → `rol.id`
- `medico.usuario_id` → `usuario.id`
- `medico.especialidad_id` → `especialidad.id`
- `paciente.usuario_id` → `usuario.id`
- `cita.paciente_id` → `paciente.id`
- `cita.medico_id` → `medico.id`
- `cita.consultorio_id` → `consultorio.id`
- `cita.estado_id` → `estado_cita.id`
- `calificacion.cita_id` → `cita.id`
- `calificacion.paciente_id` → `paciente.id`
- `calificacion.medico_id` → `medico.id`
- `notificacion.usuario_id` → `usuario.id`
- `notificacion.cita_id` → `cita.id`

### Restricciones de Unicidad:

- `usuario.email` (único)
- `medico.numero_licencia` (único)
- `medico.usuario_id` (único)
- `paciente.usuario_id` (único)
- `especialidad.nombre` (único)
- `consultorio.nombre` (único)
- `rol.nombre` (único)
- `estado_cita.nombre` (único)
- `calificacion.cita_id` (único)
- Combinación única: `cita(medico_id, fecha, hora_inicio)`
- Combinación única: `cita(consultorio_id, fecha, hora_inicio)`

### Restricciones de Dominio:

- Calificaciones entre 1 y 5
- Años de experiencia entre 0 y 50
- Duración de cita entre 15 y 180 minutos
- Capacidad de consultorio entre 1 y 10
- Precios mayores o iguales a 0
- Fecha de cita no puede ser anterior a hoy
- Hora de fin debe ser posterior a hora de inicio
- Email debe seguir formato válido
- Longitudes de texto según especificaciones

### Restricciones de Integridad Referencial:

- Eliminación en cascada para relaciones padre-hijo
- Restricción para evitar eliminación de registros referenciados
- Validación de existencia de claves foráneas


### Entidades Identificadas:

1. **USUARIO** - Entidad principal que representa a cualquier persona en el sistema
2. **MEDICO** - Especialización de USUARIO para profesionales médicos
3. **PACIENTE** - Especialización de USUARIO para pacientes
4. **ESPECIALIDAD** - Catálogo de especialidades médicas
5. **CONSULTORIO** - Espacios físicos para consultas
6. **CITA** - Entidad central que conecta médicos, pacientes y consultorios
7. **CALIFICACION** - Evaluaciones de los pacientes hacia los médicos
8. **NOTIFICACION** - Mensajes del sistema a los usuarios
9. **ROL** - Roles de usuario en el sistema
10. **ESTADO_CITA** - Estados posibles de una cita

### Atributos Clave:

- **Claves Primarias (PK)**: Todas las entidades tienen un UUID como clave primaria
- **Claves Únicas (UK)**: email (USUARIO), numero_licencia (MEDICO), nombre (ESPECIALIDAD, CONSULTORIO, ROL, ESTADO_CITA)

### Relaciones y Cardinalidades:

- **USUARIO** → **MEDICO**: 1:0..1 (Un usuario puede ser médico o no)
- **USUARIO** → **PACIENTE**: 1:0..1 (Un usuario puede ser paciente o no)
- **MEDICO** → **ESPECIALIDAD**: N:1 (Un médico tiene una especialidad, una especialidad puede tener muchos médicos)
- **MEDICO** → **CITA**: 1:N (Un médico puede tener muchas citas)
- **PACIENTE** → **CITA**: 1:N (Un paciente puede tener muchas citas)
- **CONSULTORIO** → **CITA**: 1:N (Un consultorio puede albergar muchas citas)
- **CITA** → **CALIFICACION**: 1:0..1 (Una cita puede tener una calificación o no)
- **CITA** → **NOTIFICACION**: 1:N (Una cita puede generar muchas notificaciones)

### Generalización/Especialización:

- **USUARIO** es la entidad padre
- **MEDICO** y **PACIENTE** son especializaciones de USUARIO
- Implementación mediante herencia de tabla (cada especialización tiene su propia tabla con FK a USUARIO)

### Participación:

- **Total**: MEDICO y PACIENTE deben estar relacionados con un USUARIO
- **Parcial**: CONSULTORIO en CITA (una cita puede no tener consultorio asignado)
- **Total**: CITA debe tener PACIENTE, MEDICO y ESTADO_CITA


### Tabla de Entidades

| Entidad          | Descripción                   | Atributos Clave                                                         |
| ---------------- | ----------------------------- | ----------------------------------------------------------------------- |
| **USUARIO**      | Entidad principal del sistema | id (PK), email (UK), nombre, apellidos, rol_id (FK)                     |
| **MEDICO**       | Profesional médico            | id (PK), numero_licencia (UK), usuario_id (FK), especialidad_id (FK)    |
| **PACIENTE**     | Paciente del sistema          | id (PK), usuario_id (FK), tipo_sangre, alergias                         |
| **ESPECIALIDAD** | Especialidades médicas        | id (PK), nombre (UK), duracion_cita_default, precio_base                |
| **CONSULTORIO**  | Espacios de consulta          | id (PK), nombre (UK), capacidad, equipamiento                           |
| **CITA**         | Citas médicas                 | id (PK), fecha, hora_inicio, hora_fin, paciente_id (FK), medico_id (FK) |
| **CALIFICACION** | Evaluaciones                  | id (PK), calificacion, cita_id (FK), paciente_id (FK), medico_id (FK)   |
| **NOTIFICACION** | Mensajes del sistema          | id (PK), titulo, mensaje, usuario_id (FK)                               |
| **ROL**          | Roles de usuario              | id (PK), nombre (UK), descripcion                                       |
| **ESTADO_CITA**  | Estados de citas              | id (PK), nombre (UK), color                                             |

### Tabla de Relaciones

| Relación                     | Entidades             | Cardinalidad | Participación                          |
| ---------------------------- | --------------------- | ------------ | -------------------------------------- |
| **ES_MEDICO**                | USUARIO ↔ MEDICO      | 1:0..1       | Total en MEDICO, Parcial en USUARIO    |
| **ES_PACIENTE**              | USUARIO ↔ PACIENTE    | 1:0..1       | Total en PACIENTE, Parcial en USUARIO  |
| **PERTENECE_A_ESPECIALIDAD** | MEDICO ↔ ESPECIALIDAD | N:1          | Total en ambas                         |
| **SOLICITA_CITA**            | PACIENTE ↔ CITA       | 1:N          | Total en ambas                         |
| **ATIENDE_CITA**             | MEDICO ↔ CITA         | 1:N          | Total en ambas                         |
| **SE_REALIZA_EN**            | CITA ↔ CONSULTORIO    | N:1          | Parcial en CITA, Total en CONSULTORIO  |
| **TIENE_ESTADO**             | CITA ↔ ESTADO_CITA    | N:1          | Total en ambas                         |
| **EVALUA_CITA**              | CALIFICACION ↔ CITA   | 1:1          | Total en CALIFICACION, Parcial en CITA |



## Tabla de Entidades

| Nombre de Entidad | Descripción                                                                                                              | Atributos                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **USUARIO**       | Entidad principal que representa a cualquier persona que interactúa con el sistema (médicos, pacientes, administradores) | **id** (UUID, PK), **email** (string, UK), **nombre** (string), **apellidos** (string), **telefono** (string), **fecha_nacimiento** (date), **genero** (enum), **direccion** (string), **documento_identidad** (string), **tipo_documento** (enum), **activo** (boolean), **email_verificado** (boolean), **rol_id** (UUID, FK), **ultimo_login** (datetime), **created_at** (datetime), **updated_at** (datetime)                                         |
| **MEDICO**        | Especialización de USUARIO que representa a profesionales médicos del sistema                                            | **id** (UUID, PK), **numero_licencia** (string, UK), **universidad** (string), **anos_experiencia** (int), **biografia** (string), **precio_consulta** (decimal), **disponible** (boolean), **calificacion_promedio** (decimal), **total_consultas** (int), **usuario_id** (UUID, FK), **especialidad_id** (UUID, FK), **created_at** (datetime), **updated_at** (datetime)                                                                                |
| **PACIENTE**      | Especialización de USUARIO que representa a pacientes del sistema                                                        | **id** (UUID, PK), **tipo_sangre** (string), **alergias** (string), **enfermedades_cronicas** (string), **medicamentos_actuales** (string), **contacto_emergencia_nombre** (string), **contacto_emergencia_telefono** (string), **seguro_medico** (string), **numero_seguro** (string), **usuario_id** (UUID, FK), **created_at** (datetime), **updated_at** (datetime)                                                                                    |
| **ESPECIALIDAD**  | Catálogo de especialidades médicas disponibles en el sistema                                                             | **id** (UUID, PK), **nombre** (string, UK), **descripcion** (string), **duracion_cita_default** (int), **precio_base** (decimal), **activo** (boolean), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                               |
| **CONSULTORIO**   | Espacios físicos donde se realizan las consultas médicas                                                                 | **id** (UUID, PK), **nombre** (string, UK), **descripcion** (string), **ubicacion** (string), **capacidad** (int), **equipamiento** (string), **activo** (boolean), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                   |
| **CITA**          | Entidad central que representa las citas médicas entre pacientes y médicos                                               | **id** (UUID, PK), **fecha** (date), **hora_inicio** (time), **hora_fin** (time), **motivo_consulta** (string), **observaciones_medico** (string), **diagnostico** (string), **tratamiento** (string), **precio** (decimal), **pagado** (boolean), **recordatorio_enviado** (boolean), **paciente_id** (UUID, FK), **medico_id** (UUID, FK), **consultorio_id** (UUID, FK), **estado_id** (UUID, FK), **created_at** (datetime), **updated_at** (datetime) |
| **CALIFICACION**  | Evaluaciones que los pacientes realizan sobre los médicos después de una cita                                            | **id** (UUID, PK), **calificacion** (int), **comentario** (string), **cita_id** (UUID, FK), **paciente_id** (UUID, FK), **medico_id** (UUID, FK), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                                     |
| **NOTIFICACION**  | Mensajes del sistema dirigidos a los usuarios                                                                            | **id** (UUID, PK), **titulo** (string), **mensaje** (string), **tipo** (enum), **leida** (boolean), **usuario_id** (UUID, FK), **cita_id** (UUID, FK), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                                |
| **ROL**           | Roles de usuario en el sistema (administrador, médico, paciente)                                                         | **id** (UUID, PK), **nombre** (string, UK), **descripcion** (string), **activo** (boolean), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                                                                                           |
| **ESTADO_CITA**   | Estados posibles de una cita (programada, confirmada, completada, cancelada)                                             | **id** (UUID, PK), **nombre** (string, UK), **descripcion** (string), **color** (string), **activo** (boolean), **created_at** (datetime), **updated_at** (datetime)                                                                                                                                                                                                                                                                                       |

## Tabla de Relaciones

| Nombre de Relación           | Descripción                                   | Entidades Participantes | Cardinalidad | Participación                            |
| ---------------------------- | --------------------------------------------- | ----------------------- | ------------ | ---------------------------------------- |
| **ES_MEDICO**                | Relación que indica si un usuario es médico   | USUARIO ↔ MEDICO        | 1:0..1       | Total en MEDICO, Parcial en USUARIO      |
| **ES_PACIENTE**              | Relación que indica si un usuario es paciente | USUARIO ↔ PACIENTE      | 1:0..1       | Total en PACIENTE, Parcial en USUARIO    |
| **TIENE_ROL**                | Relación que asigna un rol a un usuario       | USUARIO ↔ ROL           | N:1          | Total en USUARIO, Total en ROL           |
| **PERTENECE_A_ESPECIALIDAD** | Relación entre médico y su especialidad       | MEDICO ↔ ESPECIALIDAD   | N:1          | Total en MEDICO, Total en ESPECIALIDAD   |
| **SOLICITA_CITA**            | Relación entre paciente y cita                | PACIENTE ↔ CITA         | 1:N          | Total en PACIENTE, Total en CITA         |
| **ATIENDE_CITA**             | Relación entre médico y cita                  | MEDICO ↔ CITA           | 1:N          | Total en MEDICO, Total en CITA           |
| **SE_REALIZA_EN**            | Relación entre cita y consultorio             | CITA ↔ CONSULTORIO      | N:1          | Parcial en CITA, Total en CONSULTORIO    |
| **TIENE_ESTADO**             | Relación entre cita y su estado               | CITA ↔ ESTADO_CITA      | N:1          | Total en CITA, Total en ESTADO_CITA      |
| **EVALUA_CITA**              | Relación entre calificación y cita            | CALIFICACION ↔ CITA     | 1:1          | Total en CALIFICACION, Parcial en CITA   |
| **CALIFICA_MEDICO**          | Relación entre paciente y calificación        | PACIENTE ↔ CALIFICACION | 1:N          | Total en PACIENTE, Total en CALIFICACION |
| **RECIBE_CALIFICACION**      | Relación entre médico y calificación          | MEDICO ↔ CALIFICACION   | 1:N          | Total en MEDICO, Total en CALIFICACION   |
| **RECIBE_NOTIFICACION**      | Relación entre usuario y notificación         | USUARIO ↔ NOTIFICACION  | 1:N          | Total en USUARIO, Total en NOTIFICACION  |
| **GENERA_NOTIFICACION**      | Relación entre cita y notificación            | CITA ↔ NOTIFICACION     | 1:N          | Parcial en CITA, Total en NOTIFICACION   |

## Descripción Detallada de Atributos

### Atributos Simples:

- **id**: Identificador único universal (UUID)
- **email**: Dirección de correo electrónico del usuario
- **nombre**: Nombre de pila de la persona
- **apellidos**: Apellidos de la persona
- **telefono**: Número de teléfono de contacto
- **fecha_nacimiento**: Fecha de nacimiento
- **genero**: Género de la persona (Masculino, Femenino, Otro, Prefiero no decir)
- **direccion**: Dirección física de residencia
- **documento_identidad**: Número de documento de identidad
- **tipo_documento**: Tipo de documento (CC, CE, PP, TI)
- **activo**: Indica si el registro está activo
- **email_verificado**: Indica si el email ha sido verificado
- **numero_licencia**: Número de licencia médica
- **universidad**: Universidad donde estudió el médico
- **anos_experiencia**: Años de experiencia profesional
- **biografia**: Biografía profesional del médico
- **precio_consulta**: Precio por consulta
- **disponible**: Indica si el médico está disponible
- **calificacion_promedio**: Calificación promedio del médico
- **total_consultas**: Total de consultas realizadas
- **tipo_sangre**: Tipo de sangre del paciente
- **alergias**: Alergias conocidas del paciente
- **enfermedades_cronicas**: Enfermedades crónicas del paciente
- **medicamentos_actuales**: Medicamentos que toma actualmente
- **contacto_emergencia_nombre**: Nombre del contacto de emergencia
- **contacto_emergencia_telefono**: Teléfono del contacto de emergencia
- **seguro_medico**: Compañía de seguro médico
- **numero_seguro**: Número de póliza de seguro
- **nombre**: Nombre de la especialidad/consultorio/rol/estado
- **descripcion**: Descripción detallada
- **duracion_cita_default**: Duración por defecto de las citas
- **precio_base**: Precio base de la especialidad
- **ubicacion**: Ubicación física del consultorio
- **capacidad**: Capacidad máxima del consultorio
- **equipamiento**: Equipamiento disponible en el consultorio
- **fecha**: Fecha de la cita
- **hora_inicio**: Hora de inicio de la cita
- **hora_fin**: Hora de fin de la cita
- **motivo_consulta**: Motivo de la consulta
- **observaciones_medico**: Observaciones del médico
- **diagnostico**: Diagnóstico realizado
- **tratamiento**: Tratamiento prescrito
- **precio**: Precio de la consulta
- **pagado**: Indica si la consulta ha sido pagada
- **recordatorio_enviado**: Indica si se envió recordatorio
- **calificacion**: Calificación del 1 al 5
- **comentario**: Comentario sobre la calificación
- **titulo**: Título de la notificación
- **mensaje**: Mensaje de la notificación
- **tipo**: Tipo de notificación (info, warning, error, success)
- **leida**: Indica si la notificación ha sido leída
- **color**: Color asociado al estado
- **ultimo_login**: Último acceso al sistema
- **created_at**: Fecha de creación del registro
- **updated_at**: Fecha de última actualización

### Atributos Compuestos:

- **direccion**: Compuesto por calle, número, ciudad, código postal
- **contacto_emergencia**: Compuesto por nombre y teléfono
- **horario_cita**: Compuesto por hora_inicio y hora_fin

### Atributos Multivaluados:

- **alergias**: Lista de alergias separadas por comas
- **enfermedades_cronicas**: Lista de enfermedades separadas por comas
- **medicamentos_actuales**: Lista de medicamentos separados por comas
- **equipamiento**: Lista de equipos separados por comas

## Restricciones de Integridad

### Restricciones de Dominio:

- **calificacion**: Debe estar entre 1 y 5
- **anos_experiencia**: Debe estar entre 0 y 50
- **duracion_cita_default**: Debe estar entre 15 y 180 minutos
- **capacidad**: Debe estar entre 1 y 10 personas
- **precio_consulta, precio_base, precio**: Deben ser mayores o iguales a 0
- **email**: Debe seguir formato de email válido
- **password**: Debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número

### Restricciones de Entidad:

- **id**: No puede ser nulo, debe ser único
- **email**: No puede ser nulo, debe ser único
- **nombre**: No puede ser nulo, mínimo 2 caracteres, máximo 100
- **apellidos**: No puede ser nulo, mínimo 2 caracteres, máximo 100
- **numero_licencia**: No puede ser nulo, debe ser único, mínimo 5 caracteres
- **fecha**: No puede ser anterior a la fecha actual
- **hora_fin**: Debe ser posterior a hora_inicio

### Restricciones de Referencia:

- **usuario_id** en MEDICO debe existir en USUARIO
- **usuario_id** en PACIENTE debe existir en USUARIO
- **especialidad_id** en MEDICO debe existir en ESPECIALIDAD
- **paciente_id** en CITA debe existir en PACIENTE
- **medico_id** en CITA debe existir en MEDICO
- **consultorio_id** en CITA debe existir en CONSULTORIO (opcional)
- **estado_id** en CITA debe existir en ESTADO_CITA
- **rol_id** en USUARIO debe existir en ROL
- **cita_id** en CALIFICACION debe existir en CITA
- **paciente_id** en CALIFICACION debe existir en PACIENTE
- **medico_id** en CALIFICACION debe existir en MEDICO
- **usuario_id** en NOTIFICACION debe existir en USUARIO
- **cita_id** en NOTIFICACION debe existir en CITA (opcional)
