from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.Symptom import Symptom
from app.routers.Symptoms.model.SymptomDto import SymptomDto
from typing import List


router = APIRouter()

@router.get("/symptoms", response_model=List[SymptomDto])
def testsymtoms(db: Session = Depends(get_db)):
    sintomas = db.query(Symptom).all()
    return sintomas

@router.post("/symptoms/create", response_model=SymptomDto)
def create_symptom(symptom: SymptomDto, db: Session = Depends(get_db)):
    status = 'bad'
    try:
        symptom_dict = symptom.dict(exclude_unset=True)
        db_symptom = Symptom(**symptom_dict)
        db.add(db_symptom)
        db.commit()
        db.refresh(db_symptom)
        status = "ok"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el síntoma") from e
    return db_symptom

@router.get("/symptoms/{id}", response_model=SymptomDto)
def find_symptom_by_id(id: int, db: Session = Depends(get_db)):
    try:
        symptom = db.query(Symptom).filter(Symptom.id == id).first()
        if symptom is None:
            raise HTTPException(status_code=404, detail="Síntoma no encontrado")
        return symptom
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el síntoma") from e

@router.put("/symptoms/edit/{id}", response_model=SymptomDto)
def edit_symptom(id: int, symptom: SymptomDto, db: Session = Depends(get_db)):
    try:
        db_symptom = db.query(Symptom).filter(Symptom.id == id).first()
        if db_symptom is None:
            raise HTTPException(status_code=404, detail="Síntoma no encontrado")
        symptom_data = symptom.dict(exclude_unset=True)
        symptom_data.pop('id', None)  
        for key, value in symptom_data.items():
            setattr(db_symptom, key, value)
        db.commit()
        db.refresh(db_symptom)
        return db_symptom
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al editar el síntoma") from e

@router.delete("/symptoms/delete/{id}")
def delete_symptom(id: int, db: Session = Depends(get_db)):
    try:
        db_symptom = db.query(Symptom).filter(Symptom.id == id).first()
        if db_symptom is None:
            raise HTTPException(status_code=404, detail="Síntoma no encontrado")
        db.delete(db_symptom)
        db.commit()
        return {"message": "Síntoma eliminado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el síntoma") from e
