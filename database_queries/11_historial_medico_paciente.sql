-- ============================================
-- SCRIPT 11: Historial Médico Completo de un Paciente
-- ============================================
-- Descripción: Obtiene el historial completo de citas de un paciente específico
-- NOTA: Reemplazar 'ID_DEL_PACIENTE' con el UUID real del paciente

SELECT 
    c.fecha,
    c.hora_inicio,
    um.nombre || ' ' || um.apellidos as medico,
    e.nombre as especialidad,
    ec.nombre as estado,
    c.motivo_consulta,
    c.diagnostico,
    c.tratamiento,
    c.medicamentos_recetados,
    c.observaciones_medico,
    c.precio,
    c.pagado,
    con.nombre as consultorio,
    cal.calificacion,
    cal.comentario as comentario_calificacion
FROM public.citas c
INNER JOIN public.medicos m ON c.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
INNER JOIN public.estados_cita ec ON c.estado_id = ec.id
LEFT JOIN public.consultorios con ON c.consultorio_id = con.id
LEFT JOIN public.calificaciones cal ON c.id = cal.cita_id
WHERE c.paciente_id = 'ID_DEL_PACIENTE'  -- Reemplazar con UUID real
ORDER BY c.fecha DESC, c.hora_inicio DESC;
