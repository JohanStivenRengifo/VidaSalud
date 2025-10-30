-- ============================================
-- SCRIPT 10: Citas Próximas Sin Recordatorio Enviado
-- ============================================
-- Descripción: Lista citas programadas para los próximos 7 días 
-- que aún no tienen recordatorio enviado

SELECT 
    c.id as cita_id,
    c.fecha,
    c.hora_inicio,
    c.fecha - CURRENT_DATE as dias_hasta_cita,
    up.nombre || ' ' || up.apellidos as paciente,
    up.email as email_paciente,
    up.telefono as telefono_paciente,
    um.nombre || ' ' || um.apellidos as medico,
    e.nombre as especialidad,
    con.nombre as consultorio,
    c.motivo_consulta
FROM public.citas c
INNER JOIN public.pacientes p ON c.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.medicos m ON c.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
LEFT JOIN public.consultorios con ON c.consultorio_id = con.id
WHERE c.recordatorio_enviado = false
  AND c.fecha BETWEEN CURRENT_DATE AND CURRENT_DATE + interval '7 days'
  AND c.estado_id IN (SELECT id FROM public.estados_cita WHERE nombre = 'Programada')
ORDER BY c.fecha, c.hora_inicio;
