-- ============================================
-- SCRIPT 12: Reporte Mensual de Citas
-- ============================================
-- Descripción: Estadísticas de citas del mes actual

SELECT 
    DATE_TRUNC('day', c.fecha) as fecha,
    TO_CHAR(c.fecha, 'Day') as dia_semana,
    COUNT(*) as total_citas,
    COUNT(CASE WHEN ec.nombre = 'Programada' THEN 1 END) as programadas,
    COUNT(CASE WHEN ec.nombre = 'Completada' THEN 1 END) as completadas,
    COUNT(CASE WHEN ec.nombre = 'Cancelada' THEN 1 END) as canceladas,
    COUNT(CASE WHEN ec.nombre = 'No Asistió' THEN 1 END) as no_asistencias,
    COUNT(CASE WHEN c.pagado = true THEN 1 END) as pagadas,
    COALESCE(SUM(CASE WHEN c.pagado = true THEN c.precio ELSE 0 END), 0) as ingresos_dia,
    ROUND(AVG(c.duracion), 0) as duracion_promedio_minutos
FROM public.citas c
INNER JOIN public.estados_cita ec ON c.estado_id = ec.id
WHERE c.fecha >= DATE_TRUNC('month', CURRENT_DATE)
  AND c.fecha < DATE_TRUNC('month', CURRENT_DATE) + interval '1 month'
GROUP BY DATE_TRUNC('day', c.fecha), TO_CHAR(c.fecha, 'Day')
ORDER BY fecha;
