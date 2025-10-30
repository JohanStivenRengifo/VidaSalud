-- ============================================
-- SCRIPT 14: Notificaciones Pendientes por Usuario
-- ============================================
-- Descripción: Muestra todas las notificaciones no leídas agrupadas por usuario

SELECT 
    u.id as usuario_id,
    u.nombre || ' ' || u.apellidos as usuario,
    u.email,
    r.nombre as rol,
    COUNT(*) as notificaciones_pendientes,
    COUNT(CASE WHEN n.tipo = 'info' THEN 1 END) as info,
    COUNT(CASE WHEN n.tipo = 'warning' THEN 1 END) as warning,
    COUNT(CASE WHEN n.tipo = 'error' THEN 1 END) as error,
    COUNT(CASE WHEN n.tipo = 'success' THEN 1 END) as success,
    MIN(n.created_at) as notificacion_mas_antigua,
    MAX(n.created_at) as notificacion_mas_reciente
FROM public.usuarios u
INNER JOIN public.roles r ON u.rol_id = r.id
INNER JOIN public.notificaciones n ON u.id = n.usuario_id
WHERE n.leida = false
  AND u.activo = true
GROUP BY u.id, u.nombre, u.apellidos, u.email, r.nombre
ORDER BY notificaciones_pendientes DESC;

-- Detalle de notificaciones pendientes
SELECT 
    n.id,
    u.nombre || ' ' || u.apellidos as usuario,
    n.titulo,
    n.mensaje,
    n.tipo,
    n.created_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - n.created_at))/3600 as horas_desde_creacion,
    CASE 
        WHEN n.cita_id IS NOT NULL THEN 'Relacionada con cita'
        ELSE 'General'
    END as categoria
FROM public.notificaciones n
INNER JOIN public.usuarios u ON n.usuario_id = u.id
WHERE n.leida = false
ORDER BY n.created_at DESC;
