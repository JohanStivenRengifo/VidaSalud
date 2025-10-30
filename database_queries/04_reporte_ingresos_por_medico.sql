-- ============================================
-- SCRIPT 04: Reporte de Ingresos por Médico
-- ============================================
-- Descripción: Calcula los ingresos totales generados por cada médico
-- en citas completadas y pagadas

SELECT 
    m.id,
    u.nombre || ' ' || u.apellidos as medico,
    e.nombre as especialidad,
    COUNT(c.id) as total_citas,
    COUNT(CASE WHEN c.pagado = true THEN 1 END) as citas_pagadas,
    COUNT(CASE WHEN c.pagado = false THEN 1 END) as citas_pendientes,
    COALESCE(SUM(CASE WHEN c.pagado = true THEN c.precio ELSE 0 END), 0) as ingresos_totales,
    COALESCE(SUM(CASE WHEN c.pagado = false THEN c.precio ELSE 0 END), 0) as ingresos_pendientes,
    ROUND(AVG(c.precio), 2) as precio_promedio
FROM public.medicos m
INNER JOIN public.usuarios u ON m.usuario_id = u.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
LEFT JOIN public.citas c ON m.id = c.medico_id 
    AND c.estado_id IN (SELECT id FROM public.estados_cita WHERE nombre = 'Completada')
GROUP BY m.id, u.nombre, u.apellidos, e.nombre
ORDER BY ingresos_totales DESC;
