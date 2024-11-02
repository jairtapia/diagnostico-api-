from sqlalchemy import Column, SmallInteger, String, ForeignKey,DateTime,Time
from sqlalchemy.orm import relationship
from app.db.database import Base

class ClinicRoom(Base):
    __tablename__ = 'clinic_room'
    id = Column(SmallInteger, primary_key=True,index=True,autoincrement=True)
    numero = Column(SmallInteger, nullable=False)

    


class ClinicRoomSchedule(Base):
    __tablename__ = 'clinic_room_schedule'
    id = Column(SmallInteger, primary_key=True,index=True,autoincrement=True)
    clinic_room_id = Column(SmallInteger, ForeignKey('clinic_room.id'), nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String(10), nullable=False)



class Appointment(Base):
    __tablename__ = 'appointment'
    
    id = Column(SmallInteger, primary_key=True,index=True,autoincrement=True)
    date = Column(DateTime, nullable=False)
    time = Column(Time, nullable=False)
    patient_id = Column(SmallInteger, ForeignKey('Patient.patient_id'), nullable=False)
    doctor_id = Column(SmallInteger, ForeignKey('User.user_id'), nullable=False)
    clinic_room_id = Column(SmallInteger, ForeignKey('clinic_room.id'), nullable=False)


