-- ============================================
-- SCRIPT 06: Pacientes Más Frecuentes
-- ============================================
-- Descripción: Lista los pacientes con más citas realizadas en el sistema

SELECT 
    p.id,
    u.nombre || ' ' || u.apellidos as paciente,
    u.email,
    u.telefono,
    u.fecha_nacimiento,
    EXTRACT(YEAR FROM AGE(u.fecha_nacimiento)) as edad,
    COUNT(c.id) as total_citas,
    COUNT(CASE WHEN ec.nombre = 'Completada' THEN 1 END) as citas_completadas,
    COUNT(CASE WHEN ec.nombre = 'Cancelada' THEN 1 END) as citas_canceladas,
    COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) as no_asistencias,
    MAX(c.fecha) as ultima_cita,
    COALESCE(SUM(c.precio), 0) as total_gastado,
    p.seguro_medico
FROM public.pacientes p
INNER JOIN public.usuarios u ON p.usuario_id = u.id
LEFT JOIN public.citas c ON p.id = c.paciente_id
LEFT JOIN public.estados_cita ec ON c.estado_id = ec.id
GROUP BY p.id, u.nombre, u.apellidos, u.email, u.telefono, 
         u.fecha_nacimiento, p.seguro_medico
HAVING COUNT(c.id) > 0
ORDER BY total_citas DESC
LIMIT 20;
