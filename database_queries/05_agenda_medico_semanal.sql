-- ============================================
-- SCRIPT 05: Agenda Semanal de un Médico
-- ============================================
-- Descripción: Muestra la agenda de la semana actual para un médico específico
-- NOTA: Reemplazar 'ID_DEL_MEDICO' con el UUID real del médico

SELECT 
    c.fecha,
    TO_CHAR(c.fecha, 'Day') as dia_semana,
    c.hora_inicio,
    c.hora_fin,
    c.duracion,
    up.nombre || ' ' || up.apellidos as paciente,
    up.telefono as telefono_paciente,
    ec.nombre as estado,
    ec.color,
    c.motivo_consulta,
    con.nombre as consultorio,
    c.pagado
FROM public.citas c
INNER JOIN public.pacientes p ON c.paciente_id = p.id
INNER JOIN public.usuarios up ON p.usuario_id = up.id
INNER JOIN public.estados_cita ec ON c.estado_id = ec.id
LEFT JOIN public.consultorios con ON c.consultorio_id = con.id
WHERE c.medico_id = 'ID_DEL_MEDICO'  -- Reemplazar con UUID real
  AND c.fecha >= date_trunc('week', CURRENT_DATE)
  AND c.fecha < date_trunc('week', CURRENT_DATE) + interval '7 days'
ORDER BY c.fecha, c.hora_inicio;
