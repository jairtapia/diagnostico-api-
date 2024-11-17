from pydantic import BaseModel,Field
from typing import Optional
from datetime import date
class DiagnosticDto(BaseModel):
    id:Optional[int] = Field(default=None)
    paciente:int
    medico:int
    fecha:date
    descripcion:str
    receta:str
    enfermedad:int
    estado:int
    class Config:
        orm_mode = True

class PatientDiagnosticBase(BaseModel):
    id: Optional[int] = None
    patient_id: int
    diagnostic_id: int