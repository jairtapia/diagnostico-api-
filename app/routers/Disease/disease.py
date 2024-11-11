from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.Disease import Disease
from app.routers.Disease.model.DiseaseDto import DiseaseDto
from typing import List

router = APIRouter()

@router.get("/disease", response_model=List[DiseaseDto])
def get_diseases(db: Session = Depends(get_db)):
    enfermedades = db.query(Disease).all()
    return enfermedades