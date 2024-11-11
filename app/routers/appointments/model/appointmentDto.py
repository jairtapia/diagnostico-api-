from pydantic import BaseModel
from datetime import datetime,time
from typing import Optional

class AppointmentDto(BaseModel):
    id: Optional[int] = None
    date: datetime
    time: time
    patient_id: int
    doctor_id: int
    clinic_room_id: int

    class Config:
        orm_mode = True