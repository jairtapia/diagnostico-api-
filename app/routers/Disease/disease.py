from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.Disease import Disease
from app.db.schemas.Symptom import SymptomDisease, Symptom
from app.db.schemas.Sign import SignDisease, Sign
from app.routers.Disease.model.DiseaseDto import DiseaseDto
from app.routers.Symptoms.model.SymptomDto import SymptomDto
from app.db.schemas.DiesaseTest import TestsDiseases,Test
from typing import List

router = APIRouter()

@router.get("/disease", response_model=List[DiseaseDto])
def get_diseases(db: Session = Depends(get_db)):
    enfermedades = db.query(Disease).all()
    return enfermedades

@router.post("/disease/create")
def Create(disease:DiseaseDto, db:Session = Depends(get_db)):
    status = 'bad'
    try:
        disease_dict = disease.dict(exclude_unset=True)
        db_disease = Disease(**disease_dict)
        db.add(db_disease)
        db.commit()
        db.refresh(db_disease)
        status = 'true'
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear la enfermedad") from e
    return db_disease

@router.get("/disease/{id}")
def Find(id:int, db:Session = Depends(get_db)):
    enfermedad = db.query(Disease).filter(Disease.id == id).first()
    if enfermedad is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfermedad no encontrada")
    return enfermedad

@router.get("/disease/find/{name}")
def Find(name:str, db:Session = Depends(get_db)):
    enfermedad = db.query(Disease).filter(Disease.name == name).first()
    if enfermedad is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfermedad no encontrada")
    return enfermedad

@router.put("/disease/edit/{id}")
def Edit(id:int, disease:DiseaseDto, db:Session = Depends(get_db)):
    enfermedad = db.query(Disease).filter(Disease.id == id).first()
    if enfermedad is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfermedad no encontrada")
    
    disease_dict = disease.dict(exclude_unset=True) 
    for key, value in disease_dict.items():
        setattr(enfermedad, key, value)
    
    try:
        db.commit()
        db.refresh(enfermedad)
        return enfermedad
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al editar la enfermedad") from e
    
@router.delete("/disease/delete/{id}")
def delete_disease(id: int, db: Session = Depends(get_db)):
    try:
        db_disease = db.query(Disease).filter(Disease.id == id).first()
        if db_disease is None:
            raise HTTPException(status_code=404, detail="Enfermedad no encontrada")
        db.delete(db_disease)
        db.commit()
        return {"message": "Enfermedad eliminada con éxito"}
    except Exception as e:
        db.rollback()  # Aseguramos que se haga rollback en caso de error
        raise HTTPException(status_code=500, detail="Error al eliminar la enfermedad") from e
    

@router.get('/disease/symptoms/{id}')
def obtener_sintomas(id: int, db: Session = Depends(get_db)):
    try:
        lista = db.query(Symptom.id, Symptom.name).join(SymptomDisease).filter(SymptomDisease.disease_id == id).all()
        if not lista:
            raise HTTPException(status_code=404, detail="No se encontraron síntomas para esta enfermedad")
        return [{"id": s[0], "name": s[1]} for s in lista]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los síntomas") from e

@router.post('/disease/create/symptoms/{id}')
def CreateListSymptoms(id: int, list: List[int], db: Session = Depends(get_db)):
    try:
        for symptom_id in list:
            new_entry = SymptomDisease(disease_id=id, symptom_id=symptom_id)
            db.add(new_entry)
        db.commit()
        return {"message": "Síntomas insertados con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar los síntomas") from e

@router.get('/disease/signs/{id}')
def obtener_signos(id: int, db: Session = Depends(get_db)):
    try:
        lista = db.query(Sign.id, Sign.name).join(SignDisease).filter(SignDisease.disease_id == id).all()
        if not lista:
            raise HTTPException(status_code=404, detail="No se encontraron síntomas para esta enfermedad")
        return [{"id": s[0], "name": s[1]} for s in lista]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los síntomas") from e
    
@router.post('/disease/create/signs/{id}')
def CreateListSigns(id: int, signs:List[int], db: Session = Depends(get_db)):
    try:
        for sign_id in signs:
            new_entry = SignDisease(disease_id=id, sign_id=sign_id)
            db.add(new_entry)
        db.commit()
        return {"message": "Signos insertados con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar los signos") from e
    
@router.delete('/disease/delete/signs/{id}')
def DeleteSignlist(id:int, db:Session = Depends(get_db)):
    try:
        result = db.query(SignDisease).filter(SignDisease.disease_id == id).delete()
        db.commit()
        if result == 0:
            raise HTTPException(status_code=404, detail="No se encontraron signos para eliminar")
        return {"message": "Signos eliminados con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar los signos") from e

@router.delete('/disease/delete/symptoms/{id}')
def DeleteSymptoms(id:int, db:Session = Depends(get_db)):
    try:
        db.query(SymptomDisease).filter(SymptomDisease.disease_id == id).delete()
        db.commit()
        return {"message": "Síntomas eliminados con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar los síntomas") from e
@router.get('/disease/test/all')
def get(db:Session = Depends(get_db)):
    result = db.query(Test).all()
    result_dict = [{"id":test.id,
                    "name":test.nombre_prueba} for test in result]
    return result_dict

@router.get('/disease/test/{id}')
def getTestDisease(id:int,db:Session = Depends(get_db)):
    result = db.query(Test).join(TestsDiseases).filter(TestsDiseases.id_disease == id).all()
    result_dict = [{"id":test.id,
                    "name":test.nombre_prueba} for test in result]
    return result_dict

@router.get('/createModel')
def CreateModel(db:Session = Depends(get_db)):
    lista = db.query(Disease).join(SymptomDisease ,SymptomDisease.disease_id == Disease.id).join(SignDisease,SignDisease.disease_id == Disease.id).filter(SymptomDisease.disease_id == Disease.id, SignDisease.disease_id == Disease.id).all()
    List = [{"nombre":Disease.name,
             "sintomas":[item.name for item in (Disease.sintomas + Disease.signos)]
             } for Disease in lista]   
    return List


    #SymptomDisease  ,, SignDisease