-- ============================================
-- SCRIPT 08: Citas Pendientes de Pago
-- ============================================
-- Descripción: Lista todas las citas completadas que aún no han sido pagadas

SELECT 
    c.id,
    c.fecha,
    up.nombre || ' ' || up.apellidos as paciente,
    up.email as email_paciente,
    up.telefono as telefono_paciente,
    um.nombre || ' ' || um.apellidos as medico,
    e.nombre as especialidad,
    c.precio,
    c.created_at as fecha_creacion,
    CURRENT_DATE - c.fecha as dias_desde_cita,
    CASE 
        WHEN CURRENT_DATE - c.fecha <= 7 THEN 'Reciente'
        WHEN CURRENT_DATE - c.fecha <= 30 THEN 'Pendiente'
        ELSE 'Vencido'
    END as estado_pago
FROM public.citas c
INNER JOIN public.pacientes p ON c.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.medicos m ON c.medico_id = m.id
INNER JOIN public.usuarios um ON m.usuario_id = um.id
INNER JOIN public.especialidades e ON m.especialidad_id = e.id
WHERE c.pagado = false
  AND c.estado_id IN (SELECT id FROM public.estados_cita WHERE nombre = 'Completada')
  AND c.precio IS NOT NULL
  AND c.precio > 0
ORDER BY c.fecha DESC;
