from pydantic import BaseModel

class DiagnosticDto(BaseModel):
    id: int
    medico: int
    paciente: int
    descripcion: str
    receta: str = None
    enfermedad: int
    estado: str
    
    class Config:
        orm_mode = True