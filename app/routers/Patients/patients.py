from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List
from app.db.schemas.patient import Patient
from app.routers.Patients.model.patient import PatientDTo


router = APIRouter()


@router.get('/Patients',response_model=List[PatientDTo])
def readPatients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron pacientes")
    return patients

@router.post("/Patient/create", response_model=PatientDTo)
def createPatient(patient: PatientDTo, db: Session = Depends(get_db)):
    status = 'bad'
    try:
        patient_dict = patient.dict(exclude_unset=True)
        patient_dict.pop('patient_id', None)
        db_patient = Patient(**patient_dict)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        status = "ok"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el paciente") from e
    return db_patient

@router.get("/Patient/find/{patient_id}", response_model=PatientDTo)
def findPatientById(id: int, db: Session = Depends(get_db)):
    try:
        patient = db.query(Patient).filter(Patient.patient_id == id).first()
        if patient is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el paciente") from e

@router.get("/Patient/find/name/{name}", response_model=PatientDTo)
def findPatientByName(name: str, db: Session = Depends(get_db)):
    try:
        patient = db.query(Patient).filter(Patient.name == name).first()
        if patient is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el paciente") from e


@router.delete("/Patient/delete/{patient_id}")
def deletePatient(id:int, db:Session = Depends(get_db)):
    try:
        db_patient = db.query(Patient).filter(Patient.patient_id == id).first()
        if db_patient is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        db.delete(db_patient)
        db.commit()
        return {"message": "Paciente eliminado con éxito"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el paciente") from e
    
@router.put("/Patient/edit/{patient_id}",response_model=PatientDTo)
def editPatient(id:int, patient:PatientDTo, db :Session = Depends(get_db)):
    try:
        db_patient = db.query(Patient).filter(Patient.patient_id == id).first()
        if db_patient is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        patient_data = patient.dict(exclude_unset=True)
        patient_data.pop('patient_id', None)  
        for key, value in patient_data.items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
        return db_patient  # Cambiado para retornar el objeto actualizado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al editar el paciente") from e