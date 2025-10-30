-- ============================================
-- SCRIPT 13: Calificaciones Recientes con Comentarios
-- ============================================
-- Descripción: Últimas 20 calificaciones recibidas con sus detalles

SELECT 
    cal.created_at as fecha_calificacion,
    cal.calificacion,
    cal.comentario,
    um.nombre || ' ' || um.apellidos as medico,
    e.nombre as especialidad,
    up.nombre || ' ' || up.apellidos as paciente,
    c.fecha as fecha_cita,
    c.motivo_consulta,
    m.calificacion_promedio as calificacion_actual_medico,
    CASE 
        WHEN cal.calificacion >= 4 THEN 'Excelente'
        WHEN cal.calificacion = 3 THEN 'Buena'
        WHEN cal.calificacion = 2 THEN 'Regular'
        ELSE 'Mala'
    END as clasificacion
FROM public.calificaciones cal
INNER JOIN public.medicos m ON cal.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
INNER JOIN public.pacientes p ON cal.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.citas c ON cal.cita_id = c.id
ORDER BY cal.created_at DESC
LIMIT 20;
