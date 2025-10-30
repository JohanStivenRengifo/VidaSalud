-- ============================================
-- SCRIPT 03: Top 10 Médicos Mejor Calificados
-- ============================================
-- Descripción: Lista los 10 médicos con mejor calificación promedio
-- que tengan al menos 5 consultas realizadas

SELECT 
    m.id,
    u.nombre || ' ' || u.apellidos as nombre_completo,
    e.nombre as especialidad,
    m.calificacion_promedio,
    m.total_consultas,
    m.precio_consulta,
    m.anos_experiencia,
    COUNT(cal.id) as total_calificaciones,
    ROUND(AVG(cal.calificacion), 2) as promedio_real
FROM public.medicos m
INNER JOIN public.usuarios u ON m.usuario_id = u.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
LEFT JOIN public.calificaciones cal ON m.id = cal.medico_id
WHERE m.disponible = true
  AND m.total_consultas >= 5
GROUP BY m.id, u.nombre, u.apellidos, e.nombre, m.calificacion_promedio, 
         m.total_consultas, m.precio_consulta, m.anos_experiencia
ORDER BY m.calificacion_promedio DESC, m.total_consultas DESC
LIMIT 10;
