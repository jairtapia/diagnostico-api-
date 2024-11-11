from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.patient import Patient
from app.db.schemas.user import User
from app.db.schemas.appointment import Appointment, ClinicRoom, ClinicRoomSchedule
from app.routers.appointments.model.appointmentDto import AppointmentDto
from typing import List,Optional
from datetime import datetime,time
from fastapi.encoders import jsonable_encoder


router = APIRouter()

@router.get("/appointments", response_model=List[AppointmentDto])
def readAppointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    if not appointments:
        raise HTTPException(status_code=404, detail="No se encontraron citas para este doctor.")
    return appointments

@router.get("/appointments/{doctor_id}")
def readAppointmentsByDoctor(doctor_id: int, db: Session = Depends(get_db)):
    # Consulta Appointment y el atributo name del paciente
    appointments = (
        db.query(Appointment, 
                 Patient.name,
                 Patient.last_name_f,
                 Patient.last_name_m,
                 Patient.state,
                 ClinicRoom.numero)
        .join(Patient)
        .join(ClinicRoom)
        .filter(Appointment.doctor_id == doctor_id)
        .all()
    )

    if not appointments:
        raise HTTPException(status_code=404, detail="No se encontraron citas para este doctor.")
    
    # Construimos el resultado usando el nombre del paciente y número de la sala
    result = []
    for appointment, patient_name,last_name_f,last_name_m,state, clinic_room_numero in appointments:
        result.append({
            "id": appointment.id,
            "date": appointment.date.isoformat(),
            "time": appointment.time,
            "doctor_id": appointment.doctor_id,
            "patient_id": appointment.patient_id,
            "clinic_room_id": appointment.clinic_room_id,
            "patient": {
                "name": patient_name,
                "seconname":last_name_f,
                "lastname":last_name_m,
                "state":state,
            },
            "clinic_room": {
                "numero": clinic_room_numero
            }
        })

    return result

@router.post("/appointments/create")
def createAppointment(appointment: AppointmentDto, db: Session = Depends(get_db)):
        cita_existente = db.query(Appointment).filter(
            Appointment.date == appointment.date,
            Appointment.time == appointment.time,
            Appointment.clinic_room_id == appointment.clinic_room_id
        ).first()
        if cita_existente:
            raise HTTPException(status_code=400, detail="Ya existe una cita en este horario.")
        new_appointment = Appointment(
            date=appointment.date,
            time=appointment.time,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            clinic_room_id=appointment.clinic_room_id
        )
        
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        
        return {
            "status": "success",
            "appointment": {
                "id": new_appointment.id,
                "doctor_id": new_appointment.doctor_id,
                "patient_id": new_appointment.patient_id,
                "time": new_appointment.time,
                "date": new_appointment.date.isoformat(),
                "clinic_room_id": new_appointment.clinic_room_id
            }
        }

@router.get("/appointments/find/{id}", response_model=AppointmentDto)
def readAppointmentById(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    return appointment

@router.delete("/appointments/delete/{id}")
def deleteAppointment(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    try:
        db.delete(appointment)
        db.commit()
        return {"status": "success", "message": "Cita eliminada exitosamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar la cita: {str(e)}")

@router.put("/appointments/update/{id}")
def updateAppointment(id: int, appointment: AppointmentDto, db: Session = Depends(get_db)):
    appointment_db = db.query(Appointment).filter(Appointment.id == id).first()
    if not appointment_db:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    
    try:
        for key, value in appointment.dict(exclude_unset=True).items():
            setattr(appointment_db, key, value)
        db.commit()
        db.refresh(appointment_db)
        
        # Crear un objeto AppointmentDto desde appointment_db
        updated_appointment = AppointmentDto(
            date=appointment_db.date,
            time=appointment_db.time,
            patient_id=appointment_db.patient_id,
            doctor_id=appointment_db.doctor_id,
            clinic_room_id=appointment_db.clinic_room_id,
            # Si tienes un campo id en AppointmentDto, inclúyelo también
            id=appointment_db.id
        )
        
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar la cita: {str(e)}")
    

@router.get('/clinicroom/{id}/schedules')  
def getClinicRoomSchedules(id: int, db: Session = Depends(get_db)):
    schedules = db.query(ClinicRoomSchedule).filter(ClinicRoomSchedule.clinic_room_id == id).all()
    if not schedules:
        raise HTTPException(status_code=404, detail="No se encontraron horarios para la sala clínica.")
    return schedules

