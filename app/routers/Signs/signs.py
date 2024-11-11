from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.Sign import Sign
from app.routers.Signs.model.SignDto import SignDto
from typing import List


router = APIRouter()

@router.get("/signs", response_model=List[SignDto])
def get_signs(db: Session = Depends(get_db)):
    signs = db.query(Sign).all()
    return signs

@router.post("/signs/create")
def CreateSign(sign:SignDto,db:Session = Depends(get_db)):
    status = 'bad'
    try:
        Sign_dict = sign.dict(exclude_unset=True)
        Sign_dict.pop('patient_id', None)
        db_sign = Sign(**Sign_dict)
        db.add(db_sign)
        db.commit()
        db.refresh(db_sign)
        status = "ok"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el paciente") from e
    return db_sign

@router.get("/signs/{id}", response_model=SignDto)
def FindById(id: int, db: Session = Depends(get_db)):
    try:
        sign = db.query(Sign).filter(Sign.id == id).first()
        if sign is None:
            raise HTTPException(status_code=404, detail="Signo no encontrado")
        return sign
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el signo") from e\
    

@router.put("/signs/edit/{id}", response_model=SignDto)
def edit_sign(id: int, sign: SignDto, db: Session = Depends(get_db)):
    try:
        db_sign = db.query(Sign).filter(Sign.id == id).first()
        if db_sign is None:
            raise HTTPException(status_code=404, detail="Signo no encontrado")
        sign_data = sign.dict(exclude_unset=True)
        sign_data.pop('id', None)  
        for key, value in sign_data.items():
            setattr(db_sign, key, value)
        db.commit()
        db.refresh(db_sign)
        return db_sign
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al editar el signo") from e

@router.delete("/signs/delete/{id}")
def delete_sign(id: int, db: Session = Depends(get_db)):
    try:
        db_sign = db.query(Sign).filter(Sign.id == id).first()
        if db_sign is None:
            raise HTTPException(status_code=404, detail="Signo no encontrado")
        db.delete(db_sign)
        db.commit()
        return {"message": "Signo eliminado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el signo") from e
