-- ============================================
-- SCRIPT 02: Citas del Día
-- ============================================
-- Descripción: Lista todas las citas programadas para hoy con información completa

SELECT 
    c.id,
    c.fecha,
    c.hora_inicio,
    c.hora_fin,
    -- Paciente
    up.nombre || ' ' || up.apellidos as paciente,
    up.telefono as telefono_paciente,
    -- Médico
    um.nombre || ' ' || um.apellidos as medico,
    e.nombre as especialidad,
    -- Consultorio
    con.nombre as consultorio,
    con.ubicacion,
    -- Estado
    ec.nombre as estado,
    ec.color as color_estado,
    c.motivo_consulta,
    c.precio,
    c.pagado
FROM public.citas c
INNER JOIN public.pacientes p ON c.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.medicos m ON c.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
LEFT JOIN public.consultorios con ON c.consultorio_id = con.id
INNER JOIN public.estados_cita ec ON c.estado_id = ec.id
WHERE c.fecha = CURRENT_DATE
ORDER BY c.hora_inicio;
