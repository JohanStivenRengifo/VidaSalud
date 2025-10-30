-- ============================================
-- SISTEMA DE RESERVAS MÉDICAS - VIDA SALUD
-- Script de Base de Datos PostgreSQL/Supabase
-- Versión: 1.0.0
-- Fecha: 30 de octubre de 2025
-- ============================================

-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLA: ROLES
-- ============================================
CREATE TABLE IF NOT EXISTS public.roles (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  nombre character varying(50) NOT NULL UNIQUE,
  descripcion character varying(500),
  permisos jsonb DEFAULT '[]'::jsonb,
  activo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT roles_pkey PRIMARY KEY (id)
);

-- Índices para roles
CREATE INDEX IF NOT EXISTS idx_roles_nombre ON public.roles(nombre);
CREATE INDEX IF NOT EXISTS idx_roles_activo ON public.roles(activo);

-- ============================================
-- TABLA: USUARIOS
-- ============================================
CREATE TABLE IF NOT EXISTS public.usuarios (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  email character varying(255) NOT NULL UNIQUE,
  password_hash character varying(255) NOT NULL,
  nombre character varying(100) NOT NULL,
  apellidos character varying(100) NOT NULL,
  telefono character varying(20),
  fecha_nacimiento date,
  genero character varying(50),
  direccion character varying(500),
  documento_identidad character varying(20),
  tipo_documento character varying(10),
  rol_id uuid NOT NULL,
  activo boolean DEFAULT true,
  email_verificado boolean DEFAULT false,
  ultimo_login timestamp with time zone,
  avatar_url text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT usuarios_pkey PRIMARY KEY (id),
  CONSTRAINT usuarios_rol_id_fkey FOREIGN KEY (rol_id) REFERENCES public.roles(id) ON DELETE RESTRICT
);

-- Índices para usuarios
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON public.usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol_id ON public.usuarios(rol_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON public.usuarios(activo);
CREATE INDEX IF NOT EXISTS idx_usuarios_documento ON public.usuarios(documento_identidad);

-- ============================================
-- TABLA: ESPECIALIDADES
-- ============================================
CREATE TABLE IF NOT EXISTS public.especialidades (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  nombre character varying(100) NOT NULL UNIQUE,
  descripcion character varying(500),
  duracion_cita_default integer DEFAULT 30 CHECK (duracion_cita_default >= 15 AND duracion_cita_default <= 180),
  precio_base numeric(10,2) DEFAULT 0 CHECK (precio_base >= 0),
  activo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT especialidades_pkey PRIMARY KEY (id)
);

-- Índices para especialidades
CREATE INDEX IF NOT EXISTS idx_especialidades_nombre ON public.especialidades(nombre);
CREATE INDEX IF NOT EXISTS idx_especialidades_activo ON public.especialidades(activo);

-- ============================================
-- TABLA: MÉDICOS
-- ============================================
CREATE TABLE IF NOT EXISTS public.medicos (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  usuario_id uuid NOT NULL UNIQUE,
  especialidad_id uuid NOT NULL,
  numero_licencia character varying(50) NOT NULL UNIQUE,
  universidad character varying(200),
  anos_experiencia integer CHECK (anos_experiencia >= 0 AND anos_experiencia <= 50),
  biografia text,
  precio_consulta numeric(10,2) CHECK (precio_consulta >= 0),
  disponible boolean DEFAULT true,
  calificacion_promedio numeric(3,2) DEFAULT 0.00 CHECK (calificacion_promedio >= 0 AND calificacion_promedio <= 5),
  total_consultas integer DEFAULT 0,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT medicos_pkey PRIMARY KEY (id),
  CONSTRAINT medicos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE,
  CONSTRAINT medicos_especialidad_id_fkey FOREIGN KEY (especialidad_id) REFERENCES public.especialidades(id) ON DELETE RESTRICT
);

-- Índices para médicos
CREATE INDEX IF NOT EXISTS idx_medicos_usuario_id ON public.medicos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_medicos_especialidad_id ON public.medicos(especialidad_id);
CREATE INDEX IF NOT EXISTS idx_medicos_disponible ON public.medicos(disponible);
CREATE INDEX IF NOT EXISTS idx_medicos_calificacion ON public.medicos(calificacion_promedio);

-- ============================================
-- TABLA: PACIENTES
-- ============================================
CREATE TABLE IF NOT EXISTS public.pacientes (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  usuario_id uuid NOT NULL UNIQUE,
  tipo_sangre character varying(10),
  alergias text,
  enfermedades_cronicas text,
  medicamentos_actuales text,
  contacto_emergencia_nombre character varying(100),
  contacto_emergencia_telefono character varying(20),
  seguro_medico character varying(100),
  numero_seguro character varying(50),
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT pacientes_pkey PRIMARY KEY (id),
  CONSTRAINT pacientes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE
);

-- Índices para pacientes
CREATE INDEX IF NOT EXISTS idx_pacientes_usuario_id ON public.pacientes(usuario_id);

-- ============================================
-- TABLA: CONSULTORIOS
-- ============================================
CREATE TABLE IF NOT EXISTS public.consultorios (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  nombre character varying(100) NOT NULL,
  descripcion text,
  ubicacion text,
  capacidad integer DEFAULT 1 CHECK (capacidad >= 1 AND capacidad <= 10),
  equipamiento text,
  activo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT consultorios_pkey PRIMARY KEY (id)
);

-- Índices para consultorios
CREATE INDEX IF NOT EXISTS idx_consultorios_activo ON public.consultorios(activo);
CREATE INDEX IF NOT EXISTS idx_consultorios_nombre ON public.consultorios(nombre);

-- ============================================
-- TABLA: ESTADOS_CITA
-- ============================================
CREATE TABLE IF NOT EXISTS public.estados_cita (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  nombre character varying(50) NOT NULL UNIQUE,
  descripcion character varying(500),
  color character varying(7) DEFAULT '#6B7280',
  orden integer DEFAULT 0,
  activo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT estados_cita_pkey PRIMARY KEY (id)
);

-- Índices para estados_cita
CREATE INDEX IF NOT EXISTS idx_estados_cita_nombre ON public.estados_cita(nombre);
CREATE INDEX IF NOT EXISTS idx_estados_cita_activo ON public.estados_cita(activo);
CREATE INDEX IF NOT EXISTS idx_estados_cita_orden ON public.estados_cita(orden);

-- ============================================
-- TABLA: CITAS
-- ============================================
CREATE TABLE IF NOT EXISTS public.citas (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  paciente_id uuid NOT NULL,
  medico_id uuid NOT NULL,
  consultorio_id uuid,
  estado_id uuid NOT NULL,
  fecha date NOT NULL CHECK (fecha >= CURRENT_DATE),
  hora_inicio time without time zone NOT NULL,
  hora_fin time without time zone NOT NULL,
  duracion integer DEFAULT 30 CHECK (duracion >= 1),
  motivo_consulta text,
  observaciones_medico text,
  diagnostico text,
  tratamiento text,
  medicamentos_recetados text,
  precio numeric(10,2) CHECK (precio >= 0),
  pagado boolean DEFAULT false,
  recordatorio_enviado boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT citas_pkey PRIMARY KEY (id),
  CONSTRAINT citas_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE,
  CONSTRAINT citas_medico_id_fkey FOREIGN KEY (medico_id) REFERENCES public.medicos(id) ON DELETE CASCADE,
  CONSTRAINT citas_consultorio_id_fkey FOREIGN KEY (consultorio_id) REFERENCES public.consultorios(id) ON DELETE SET NULL,
  CONSTRAINT citas_estado_id_fkey FOREIGN KEY (estado_id) REFERENCES public.estados_cita(id) ON DELETE RESTRICT,
  CONSTRAINT check_hora_fin CHECK (hora_fin > hora_inicio)
);

-- Índices para citas
CREATE INDEX IF NOT EXISTS idx_citas_paciente_id ON public.citas(paciente_id);
CREATE INDEX IF NOT EXISTS idx_citas_medico_id ON public.citas(medico_id);
CREATE INDEX IF NOT EXISTS idx_citas_consultorio_id ON public.citas(consultorio_id);
CREATE INDEX IF NOT EXISTS idx_citas_estado_id ON public.citas(estado_id);
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON public.citas(fecha);
CREATE INDEX IF NOT EXISTS idx_citas_fecha_hora ON public.citas(fecha, hora_inicio);
CREATE INDEX IF NOT EXISTS idx_citas_pagado ON public.citas(pagado);

-- ============================================
-- TABLA: CALIFICACIONES
-- ============================================
CREATE TABLE IF NOT EXISTS public.calificaciones (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  cita_id uuid NOT NULL UNIQUE,
  paciente_id uuid NOT NULL,
  medico_id uuid NOT NULL,
  calificacion integer NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
  comentario text,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT calificaciones_pkey PRIMARY KEY (id),
  CONSTRAINT calificaciones_cita_id_fkey FOREIGN KEY (cita_id) REFERENCES public.citas(id) ON DELETE CASCADE,
  CONSTRAINT calificaciones_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE,
  CONSTRAINT calificaciones_medico_id_fkey FOREIGN KEY (medico_id) REFERENCES public.medicos(id) ON DELETE CASCADE
);

-- Índices para calificaciones
CREATE INDEX IF NOT EXISTS idx_calificaciones_cita_id ON public.calificaciones(cita_id);
CREATE INDEX IF NOT EXISTS idx_calificaciones_paciente_id ON public.calificaciones(paciente_id);
CREATE INDEX IF NOT EXISTS idx_calificaciones_medico_id ON public.calificaciones(medico_id);
CREATE INDEX IF NOT EXISTS idx_calificaciones_calificacion ON public.calificaciones(calificacion);

-- ============================================
-- TABLA: NOTIFICACIONES
-- ============================================
CREATE TABLE IF NOT EXISTS public.notificaciones (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  usuario_id uuid NOT NULL,
  cita_id uuid,
  titulo character varying(200) NOT NULL,
  mensaje text NOT NULL,
  tipo character varying(20) DEFAULT 'info',
  leida boolean DEFAULT false,
  data jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT notificaciones_pkey PRIMARY KEY (id),
  CONSTRAINT notificaciones_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE CASCADE,
  CONSTRAINT notificaciones_cita_id_fkey FOREIGN KEY (cita_id) REFERENCES public.citas(id) ON DELETE CASCADE
);

-- Índices para notificaciones
CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario_id ON public.notificaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notificaciones_cita_id ON public.notificaciones(cita_id);
CREATE INDEX IF NOT EXISTS idx_notificaciones_leida ON public.notificaciones(leida);
CREATE INDEX IF NOT EXISTS idx_notificaciones_created_at ON public.notificaciones(created_at);

-- ============================================
-- TRIGGERS PARA ACTUALIZAR updated_at
-- ============================================

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para todas las tablas
DROP TRIGGER IF EXISTS update_roles_updated_at ON public.roles;
CREATE TRIGGER update_roles_updated_at 
  BEFORE UPDATE ON public.roles 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_usuarios_updated_at ON public.usuarios;
CREATE TRIGGER update_usuarios_updated_at 
  BEFORE UPDATE ON public.usuarios 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_especialidades_updated_at ON public.especialidades;
CREATE TRIGGER update_especialidades_updated_at 
  BEFORE UPDATE ON public.especialidades 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_medicos_updated_at ON public.medicos;
CREATE TRIGGER update_medicos_updated_at 
  BEFORE UPDATE ON public.medicos 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_pacientes_updated_at ON public.pacientes;
CREATE TRIGGER update_pacientes_updated_at 
  BEFORE UPDATE ON public.pacientes 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_consultorios_updated_at ON public.consultorios;
CREATE TRIGGER update_consultorios_updated_at 
  BEFORE UPDATE ON public.consultorios 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_estados_cita_updated_at ON public.estados_cita;
CREATE TRIGGER update_estados_cita_updated_at 
  BEFORE UPDATE ON public.estados_cita 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_citas_updated_at ON public.citas;
CREATE TRIGGER update_citas_updated_at 
  BEFORE UPDATE ON public.citas 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_calificaciones_updated_at ON public.calificaciones;
CREATE TRIGGER update_calificaciones_updated_at 
  BEFORE UPDATE ON public.calificaciones 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_notificaciones_updated_at ON public.notificaciones;
CREATE TRIGGER update_notificaciones_updated_at 
  BEFORE UPDATE ON public.notificaciones 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- FUNCIÓN PARA ACTUALIZAR CALIFICACIÓN PROMEDIO DEL MÉDICO
-- ============================================
CREATE OR REPLACE FUNCTION update_medico_calificacion()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE public.medicos
    SET calificacion_promedio = (
        SELECT COALESCE(AVG(calificacion), 0)
        FROM public.calificaciones
        WHERE medico_id = NEW.medico_id
    )
    WHERE id = NEW.medico_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_medico_calificacion ON public.calificaciones;
CREATE TRIGGER trigger_update_medico_calificacion
  AFTER INSERT OR UPDATE ON public.calificaciones
  FOR EACH ROW
  EXECUTE FUNCTION update_medico_calificacion();

-- ============================================
-- FUNCIÓN PARA INCREMENTAR TOTAL DE CONSULTAS DEL MÉDICO
-- ============================================
CREATE OR REPLACE FUNCTION increment_medico_consultas()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si el estado cambió a "Completada"
    IF NEW.estado_id IN (SELECT id FROM public.estados_cita WHERE nombre = 'Completada') 
       AND (OLD.estado_id IS NULL OR OLD.estado_id != NEW.estado_id) THEN
        UPDATE public.medicos
        SET total_consultas = total_consultas + 1
        WHERE id = NEW.medico_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_increment_medico_consultas ON public.citas;
CREATE TRIGGER trigger_increment_medico_consultas
  AFTER INSERT OR UPDATE ON public.citas
  FOR EACH ROW
  EXECUTE FUNCTION increment_medico_consultas();

-- ============================================
-- DATOS INICIALES: ROLES
-- ============================================
INSERT INTO public.roles (nombre, descripcion, permisos) VALUES
('Administrador', 'Administrador del sistema con acceso completo', '["all"]'::jsonb),
('Medico', 'Médico que puede atender pacientes', '["citas:read", "citas:update", "pacientes:read"]'::jsonb),
('Paciente', 'Paciente que puede agendar citas', '["citas:create", "citas:read", "medicos:read"]'::jsonb)
ON CONFLICT (nombre) DO NOTHING;

-- ============================================
-- DATOS INICIALES: ESTADOS DE CITA
-- ============================================
INSERT INTO public.estados_cita (nombre, descripcion, color, orden) VALUES
('Programada', 'Cita programada y confirmada', '#3B82F6', 1),
('En Progreso', 'Cita en curso', '#F59E0B', 2),
('Completada', 'Cita completada exitosamente', '#10B981', 3),
('Cancelada', 'Cita cancelada', '#EF4444', 4),
('No Asistió', 'Paciente no asistió a la cita', '#6B7280', 5)
ON CONFLICT (nombre) DO NOTHING;

-- ============================================
-- DATOS INICIALES: ESPECIALIDADES
-- ============================================
INSERT INTO public.especialidades (nombre, descripcion, duracion_cita_default, precio_base) VALUES
('Medicina General', 'Atención médica general y preventiva', 30, 50000),
('Cardiología', 'Especialidad en enfermedades del corazón', 45, 80000),
('Dermatología', 'Especialidad en enfermedades de la piel', 30, 70000),
('Pediatría', 'Especialidad en medicina infantil', 30, 60000),
('Ginecología', 'Especialidad en salud reproductiva femenina', 45, 75000),
('Odontología', 'Especialidad en salud dental', 30, 65000),
('Oftalmología', 'Especialidad en salud visual', 30, 70000),
('Psicología', 'Atención en salud mental y emocional', 60, 80000),
('Traumatología', 'Especialidad en lesiones del sistema músculo-esquelético', 30, 75000),
('Neurología', 'Especialidad en enfermedades del sistema nervioso', 45, 90000)
ON CONFLICT (nombre) DO NOTHING;

-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista de médicos con detalles
CREATE OR REPLACE VIEW vista_medicos_completa AS
SELECT 
    m.id,
    m.usuario_id,
    u.nombre,
    u.apellidos,
    u.email,
    u.telefono,
    u.avatar_url,
    m.numero_licencia,
    m.universidad,
    m.anos_experiencia,
    m.biografia,
    m.precio_consulta,
    m.disponible,
    m.calificacion_promedio,
    m.total_consultas,
    e.id as especialidad_id,
    e.nombre as especialidad_nombre,
    e.descripcion as especialidad_descripcion,
    m.created_at,
    m.updated_at
FROM public.medicos m
INNER JOIN public.usuarios u ON m.usuario_id = u.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id;

-- Vista de pacientes con detalles
CREATE OR REPLACE VIEW vista_pacientes_completa AS
SELECT 
    p.id,
    p.usuario_id,
    u.nombre,
    u.apellidos,
    u.email,
    u.telefono,
    u.fecha_nacimiento,
    u.genero,
    u.direccion,
    u.documento_identidad,
    u.tipo_documento,
    p.tipo_sangre,
    p.alergias,
    p.enfermedades_cronicas,
    p.medicamentos_actuales,
    p.contacto_emergencia_nombre,
    p.contacto_emergencia_telefono,
    p.seguro_medico,
    p.numero_seguro,
    p.created_at,
    p.updated_at
FROM public.pacientes p
INNER JOIN public.usuarios u ON p.usuario_id = u.id;

-- Vista de citas con detalles completos
CREATE OR REPLACE VIEW vista_citas_completa AS
SELECT 
    c.id,
    c.fecha,
    c.hora_inicio,
    c.hora_fin,
    c.duracion,
    c.motivo_consulta,
    c.observaciones_medico,
    c.diagnostico,
    c.tratamiento,
    c.medicamentos_recetados,
    c.precio,
    c.pagado,
    c.recordatorio_enviado,
    -- Paciente
    p.id as paciente_id,
    up.nombre as paciente_nombre,
    up.apellidos as paciente_apellidos,
    up.email as paciente_email,
    up.telefono as paciente_telefono,
    -- Médico
    m.id as medico_id,
    um.nombre as medico_nombre,
    um.apellidos as medico_apellidos,
    um.email as medico_email,
    -- Especialidad
    e.id as especialidad_id,
    e.nombre as especialidad_nombre,
    -- Consultorio
    con.id as consultorio_id,
    con.nombre as consultorio_nombre,
    con.ubicacion as consultorio_ubicacion,
    -- Estado
    ec.id as estado_id,
    ec.nombre as estado_nombre,
    ec.color as estado_color,
    c.created_at,
    c.updated_at
FROM public.citas c
INNER JOIN public.pacientes p ON c.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.medicos m ON c.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
LEFT JOIN public.consultorios con ON c.consultorio_id = con.id
INNER JOIN public.estados_cita ec ON c.estado_id = ec.id;

-- Vista de calificaciones con detalles
CREATE OR REPLACE VIEW vista_calificaciones_completa AS
SELECT 
    cal.id,
    cal.cita_id,
    cal.paciente_id,
    cal.medico_id,
    cal.calificacion,
    cal.comentario,
    cal.created_at,
    cal.updated_at,
    -- Paciente
    up.nombre as paciente_nombre,
    up.apellidos as paciente_apellidos,
    -- Médico
    um.nombre as medico_nombre,
    um.apellidos as medico_apellidos,
    -- Especialidad del médico
    e.nombre as especialidad_nombre,
    -- Fecha de la cita
    c.fecha as cita_fecha
FROM public.calificaciones cal
INNER JOIN public.pacientes p ON cal.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.medicos m ON cal.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
INNER JOIN public.citas c ON cal.cita_id = c.id;

-- ============================================
-- POLÍTICAS DE SEGURIDAD RLS (Row Level Security)
-- ============================================
-- NOTA: Habilitar RLS en Supabase según las necesidades de seguridad

-- Habilitar RLS en tablas sensibles
ALTER TABLE public.usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.medicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pacientes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.citas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.calificaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notificaciones ENABLE ROW LEVEL SECURITY;

-- Políticas de ejemplo (ajustar según necesidades)
-- Los usuarios solo pueden ver su propia información
CREATE POLICY "Usuarios pueden ver su propia información" 
  ON public.usuarios FOR SELECT 
  USING (auth.uid() = id);

-- Los médicos pueden ver sus propias citas
CREATE POLICY "Médicos pueden ver sus citas" 
  ON public.citas FOR SELECT 
  USING (
    medico_id IN (
      SELECT id FROM public.medicos WHERE usuario_id = auth.uid()
    )
  );

-- Los pacientes pueden ver sus propias citas
CREATE POLICY "Pacientes pueden ver sus citas" 
  ON public.citas FOR SELECT 
  USING (
    paciente_id IN (
      SELECT id FROM public.pacientes WHERE usuario_id = auth.uid()
    )
  );

-- Los usuarios pueden ver sus propias notificaciones
CREATE POLICY "Usuarios pueden ver sus notificaciones" 
  ON public.notificaciones FOR SELECT 
  USING (usuario_id = auth.uid());

-- ============================================
-- COMENTARIOS EN TABLAS Y COLUMNAS
-- ============================================

COMMENT ON TABLE public.roles IS 'Roles de usuarios del sistema (Administrador, Médico, Paciente)';
COMMENT ON TABLE public.usuarios IS 'Información general de todos los usuarios del sistema';
COMMENT ON TABLE public.especialidades IS 'Especialidades médicas disponibles';
COMMENT ON TABLE public.medicos IS 'Información específica de los médicos';
COMMENT ON TABLE public.pacientes IS 'Información específica de los pacientes';
COMMENT ON TABLE public.consultorios IS 'Consultorios disponibles para atención médica';
COMMENT ON TABLE public.estados_cita IS 'Estados posibles de una cita (Programada, Completada, etc.)';
COMMENT ON TABLE public.citas IS 'Citas médicas programadas';
COMMENT ON TABLE public.calificaciones IS 'Calificaciones de pacientes a médicos';
COMMENT ON TABLE public.notificaciones IS 'Notificaciones del sistema para los usuarios';