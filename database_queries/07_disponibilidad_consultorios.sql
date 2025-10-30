-- ============================================
-- SCRIPT 07: Disponibilidad de Consultorios
-- ============================================
-- Descripción: Verifica qué consultorios están ocupados y cuáles disponibles hoy

SELECT 
    con.id,
    con.nombre,
    con.ubicacion,
    con.capacidad,
    COUNT(c.id) as citas_programadas_hoy,
    con.capacidad - COUNT(c.id) as espacios_disponibles,
    CASE 
        WHEN COUNT(c.id) = 0 THEN 'Libre'
        WHEN COUNT(c.id) < con.capacidad THEN 'Parcialmente Ocupado'
        ELSE 'Ocupado'
    END as estado_disponibilidad,
    con.equipamiento
FROM public.consultorios con
LEFT JOIN public.citas c ON con.id = c.consultorio_id 
    AND c.fecha = CURRENT_DATE
    AND c.estado_id NOT IN (SELECT id FROM public.estados_cita WHERE nombre IN ('Cancelada', 'No Asistió'))
WHERE con.activo = true
GROUP BY con.id, con.nombre, con.ubicacion, con.capacidad, con.equipamiento
ORDER BY espacios_disponibles DESC, con.nombre;
