-- ============================================
-- SCRIPT 15: Análisis de Ausentismo de Pacientes
-- ============================================
-- Descripción: Identifica pacientes con alto índice de inasistencia

SELECT 
    p.id,
    u.nombre || ' ' || u.apellidos as paciente,
    u.email,
    u.telefono,
    COUNT(c.id) as total_citas_agendadas,
    COUNT(CASE WHEN ec.nombre = 'Completada' THEN 1 END) as asistencias,
    COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) as inasistencias,
    COUNT(CASE WHEN ec.nombre = 'Cancelada' THEN 1 END) as cancelaciones,
    ROUND(
        COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(c.id), 0), 2
    ) as porcentaje_inasistencia,
    ROUND(
        COUNT(CASE WHEN ec.nombre = 'Cancelada' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(c.id), 0), 2
    ) as porcentaje_cancelacion,
    CASE 
        WHEN COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) * 100.0 / NULLIF(COUNT(c.id), 0) >= 50 THEN 'Crítico'
        WHEN COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) * 100.0 / NULLIF(COUNT(c.id), 0) >= 30 THEN 'Alto'
        WHEN COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) * 100.0 / NULLIF(COUNT(c.id), 0) >= 10 THEN 'Moderado'
        ELSE 'Bajo'
    END as nivel_riesgo,
    MAX(c.fecha) as ultima_cita,
    COALESCE(SUM(CASE WHEN c.pagado = false AND ec.nombre = 'No Asistió' THEN c.precio ELSE 0 END), 0) as perdida_economica
FROM public.pacientes p
INNER JOIN public.usuarios u ON p.usuario_id = u.id
LEFT JOIN public.citas c ON p.id = c.paciente_id
LEFT JOIN public.estados_cita ec ON c.estado_id = ec.id
WHERE c.id IS NOT NULL
GROUP BY p.id, u.nombre, u.apellidos, u.email, u.telefono
HAVING COUNT(c.id) >= 3  -- Solo pacientes con al menos 3 citas
ORDER BY porcentaje_inasistencia DESC, total_citas_agendadas DESC;
