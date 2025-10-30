-- ============================================
-- SCRIPT 09: Estadísticas por Especialidad
-- ============================================
-- Descripción: Resumen de actividad y métricas por especialidad médica

SELECT 
    e.id,
    e.nombre as especialidad,
    e.precio_base,
    e.duracion_cita_default,
    COUNT(DISTINCT m.id) as total_medicos,
    COUNT(DISTINCT CASE WHEN m.disponible = true THEN m.id END) as medicos_disponibles,
    COUNT(c.id) as total_citas,
    COUNT(CASE WHEN ec.nombre = 'Completada' THEN 1 END) as citas_completadas,
    COUNT(CASE WHEN ec.nombre = 'Cancelada' THEN 1 END) as citas_canceladas,
    ROUND(AVG(m.calificacion_promedio), 2) as calificacion_promedio_especialidad,
    COALESCE(SUM(CASE WHEN c.pagado = true THEN c.precio ELSE 0 END), 0) as ingresos_totales,
    ROUND(AVG(c.precio), 2) as precio_promedio_cita,
    COUNT(DISTINCT cal.id) as total_calificaciones
FROM public.especialidades e
LEFT JOIN public.medicos m ON e.id = m.especialidad_id
LEFT JOIN public.citas c ON m.id = c.medico_id
LEFT JOIN public.estados_cita ec ON c.estado_id = ec.id
LEFT JOIN public.calificaciones cal ON m.id = cal.medico_id
WHERE e.activo = true
GROUP BY e.id, e.nombre, e.precio_base, e.duracion_cita_default
ORDER BY total_citas DESC, ingresos_totales DESC;
