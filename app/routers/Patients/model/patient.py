from pydantic import BaseModel
from typing import Optional

class PatientDTo(BaseModel):
    patient_id : Optional[int] = None
    name : str
    last_name_f: str 
    last_name_m: str 
    age : int
    phone : str
    address : str
    state : str

    class Config:
        orm_mode = True