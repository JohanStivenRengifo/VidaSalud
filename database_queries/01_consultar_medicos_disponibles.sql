-- ============================================
-- SCRIPT 01: Consultar Médicos Disponibles por Especialidad
-- ============================================
-- Descripción: Obtiene todos los médicos disponibles con su información completa,
-- ordenados por especialidad y calificación

SELECT 
    m.id,
    u.nombre || ' ' || u.apellidos as nombre_completo,
    u.email,
    u.telefono,
    e.nombre as especialidad,
    m.numero_licencia,
    m.universidad,
    m.anos_experiencia,
    m.precio_consulta,
    m.calificacion_promedio,
    m.total_consultas,
    m.biografia
FROM public.medicos m
INNER JOIN public.usuarios u ON m.usuario_id = u.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
WHERE m.disponible = true 
  AND u.activo = true
ORDER BY e.nombre, m.calificacion_promedio DESC, m.total_consultas DESC;
