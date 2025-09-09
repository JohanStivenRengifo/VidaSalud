"""
Servicio para la entidad Cita
"""
from typing import List, Optional
from uuid import UUID
from datetime import date, time, datetime, timedelta
from fastapi import HTTPException, status

from app.models.cita import Cita, CitaCreate, CitaUpdate, CitaResponse, CitaConDetalles
from app.repositories.cita_repository import CitaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository
from app.database import db_connection


class CitaService:
    """Servicio para operaciones de Cita"""
    
    def __init__(self):
        self.cita_repo = CitaRepository()
        self.medico_repo = MedicoRepository()
        self.paciente_repo = PacienteRepository()
    
    async def create_cita(self, cita_data: CitaCreate) -> CitaResponse:
        """Crear una nueva cita"""
        # Verificar que el médico existe y está disponible
        medico = await self.medico_repo.get_by_id(cita_data.medico_id)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Médico no encontrado"
            )
        
        if not medico["disponible"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El médico no está disponible"
            )
        
        # Verificar que el paciente existe
        paciente = await self.paciente_repo.get_by_id(cita_data.paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        # Verificar disponibilidad del horario
        horario_disponible = await self.cita_repo.check_horario_disponible(
            cita_data.medico_id,
            cita_data.fecha,
            cita_data.hora_inicio.isoformat(),
            cita_data.hora_fin.isoformat()
        )
        
        if not horario_disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El horario seleccionado no está disponible"
            )
        
        # Crear la cita
        cita_dict = cita_data.dict()
        created_cita = await self.cita_repo.create(cita_dict)
        if not created_cita:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear la cita"
            )
        
        return CitaResponse(**created_cita)
    
    async def get_cita(self, cita_id: UUID) -> CitaResponse:
        """Obtener una cita por ID"""
        cita = await self.cita_repo.get_by_id(cita_id)
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        return CitaResponse(**cita)
    
    async def get_citas(self, skip: int = 0, limit: int = 100) -> List[CitaResponse]:
        """Obtener lista de citas"""
        citas = await self.cita_repo.get_all(skip, limit)
        return [CitaResponse(**cita) for cita in citas]
    
    async def get_citas_with_details(self, skip: int = 0, limit: int = 100) -> List[CitaConDetalles]:
        """Obtener citas con información detallada"""
        citas = await self.cita_repo.get_with_details(skip, limit)
        return [CitaConDetalles(**cita) for cita in citas]
    
    async def update_cita(self, cita_id: UUID, cita_data: CitaUpdate) -> CitaResponse:
        """Actualizar una cita"""
        existing_cita = await self.cita_repo.get_by_id(cita_id)
        if not existing_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        
        # Si se está cambiando el horario, verificar disponibilidad
        if (cita_data.fecha or cita_data.hora_inicio or cita_data.hora_fin or cita_data.medico_id):
            medico_id = cita_data.medico_id or existing_cita["medico_id"]
            fecha = cita_data.fecha or existing_cita["fecha"]
            hora_inicio = cita_data.hora_inicio or existing_cita["hora_inicio"]
            hora_fin = cita_data.hora_fin or existing_cita["hora_fin"]
            
            # Verificar disponibilidad excluyendo la cita actual
            horario_disponible = await self.cita_repo.check_horario_disponible(
                medico_id, fecha, hora_inicio.isoformat(), hora_fin.isoformat()
            )
            
            if not horario_disponible:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El horario seleccionado no está disponible"
                )
        
        update_data = cita_data.dict(exclude_unset=True)
        updated_cita = await self.cita_repo.update(cita_id, update_data)
        if not updated_cita:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al actualizar la cita"
            )
        
        return CitaResponse(**updated_cita)
    
    async def delete_cita(self, cita_id: UUID) -> bool:
        """Eliminar una cita"""
        existing_cita = await self.cita_repo.get_by_id(cita_id)
        if not existing_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        
        return await self.cita_repo.delete(cita_id)
    
    async def get_citas_by_paciente(self, paciente_id: UUID) -> List[CitaConDetalles]:
        """Obtener citas de un paciente"""
        citas = await self.cita_repo.get_by_paciente_with_details(paciente_id)
        return [CitaConDetalles(**cita) for cita in citas]
    
    async def get_citas_by_medico(self, medico_id: UUID) -> List[CitaConDetalles]:
        """Obtener citas de un médico"""
        citas = await self.cita_repo.get_by_medico_with_details(medico_id)
        return [CitaConDetalles(**cita) for cita in citas]
    
    async def get_citas_by_fecha(self, fecha: date) -> List[CitaResponse]:
        """Obtener citas por fecha"""
        citas = await self.cita_repo.get_by_fecha(fecha)
        return [CitaResponse(**cita) for cita in citas]
    
    async def get_citas_by_fecha_range(self, fecha_inicio: date, fecha_fin: date) -> List[CitaResponse]:
        """Obtener citas en un rango de fechas"""
        citas = await self.cita_repo.get_by_fecha_range(fecha_inicio, fecha_fin)
        return [CitaResponse(**cita) for cita in citas]
    
    async def get_citas_pendientes_pago(self) -> List[CitaResponse]:
        """Obtener citas pendientes de pago"""
        citas = await self.cita_repo.get_pendientes_pago()
        return [CitaResponse(**cita) for cita in citas]
    
    async def marcar_como_pagada(self, cita_id: UUID) -> CitaResponse:
        """Marcar cita como pagada"""
        update_data = {"pagado": True}
        updated_cita = await self.cita_repo.update(cita_id, update_data)
        if not updated_cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada"
            )
        return CitaResponse(**updated_cita)
    
    async def get_horarios_disponibles(self, medico_id: UUID, fecha: date) -> List[dict]:
        """Obtener horarios disponibles para un médico en una fecha"""
        # Obtener citas existentes del médico en esa fecha
        citas_existentes = await self.cita_repo.get_by_medico_fecha(medico_id, fecha)
        
        # Obtener horarios de atención del médico
        # Aquí podrías implementar lógica para obtener horarios de atención
        # Por simplicidad, asumimos horarios de 9:00 a 17:00 con intervalos de 30 min
        
        horarios_ocupados = []
        for cita in citas_existentes:
            horarios_ocupados.append({
                "inicio": cita["hora_inicio"],
                "fin": cita["hora_fin"]
            })
        
        # Generar horarios disponibles (simplificado)
        horarios_disponibles = []
        hora_inicio = time(9, 0)
        hora_fin = time(17, 0)
        
        current_time = datetime.combine(fecha, hora_inicio)
        end_time = datetime.combine(fecha, hora_fin)
        
        while current_time < end_time:
            slot_inicio = current_time.time()
            slot_fin = (current_time + timedelta(minutes=30)).time()
            
            # Verificar si el slot está ocupado
            ocupado = any(
                slot_inicio < ocupado["fin"] and slot_fin > ocupado["inicio"]
                for ocupado in horarios_ocupados
            )
            
            if not ocupado:
                horarios_disponibles.append({
                    "hora_inicio": slot_inicio.isoformat(),
                    "hora_fin": slot_fin.isoformat()
                })
            
            current_time += timedelta(minutes=30)
        
        return horarios_disponibles
