from app.routers.Diagnostico.model.diagnostico import DiagnosticDto,PatientDiagnosticBase
from app.db.schemas.Diagnostic import Diagnostic ,PatientDiagnostic
from fastapi import APIRouter,Depends
from app.db.database import get_db
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()

@router.get('/diagnostico')
def read(db: Session = Depends(get_db)):
    diagnostics = db.query(Diagnostic).all()
    if not diagnostics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron diagnósticos")
    return diagnostics

@router.post("/diagnostico/create", response_model=DiagnosticDto)
def create_diagnostic(diagnostic: DiagnosticDto, db: Session = Depends(get_db)):
        try:
            diagnostic_dict = diagnostic.dict(exclude_unset=True)
            db_diagnostic = Diagnostic(**diagnostic_dict)
            db.add(db_diagnostic)
            db.commit()
            db.refresh(db_diagnostic)
            return db_diagnostic
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="Error al crear el diagnóstico") from e

@router.get("/diagnostico/find/{diagnostic_id}", response_model=DiagnosticDto)
def find_diagnostic_by_id(diagnostic_id: int, db: Session = Depends(get_db)):
        diagnostic = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
        if diagnostic is None:
            raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
        return diagnostic

@router.put("/diagnostico/update/{diagnostic_id}", response_model=DiagnosticDto)
def update_diagnostic(diagnostic_id: int, diagnostic: DiagnosticDto, db: Session = Depends(get_db)):
        diagnostic_db = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
        if diagnostic_db is None:
            raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
        for key, value in diagnostic.dict(exclude_unset=True).items():
            setattr(diagnostic_db, key, value)
        db.commit()
        db.refresh(diagnostic_db)
        return diagnostic_db

@router.delete("/diagnostico/delete/{diagnostic_id}")
def delete_diagnostic(diagnostic_id: int, db: Session = Depends(get_db)):
        diagnostic_db = db.query(Diagnostic).filter(Diagnostic.id == diagnostic_id).first()
        if diagnostic_db is None:
            raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
        db.delete(diagnostic_db)
        db.commit()
        return {"detail": "Diagnóstico eliminado exitosamente"}

@router.post('/diagnostic/patient')
def add_to_list(data: PatientDiagnosticBase, db: Session = Depends(get_db)):
    try:
        diagnostic_dict = data.dict(exclude_unset=True)
        db_diagnostic = PatientDiagnostic(**diagnostic_dict)
        db.add(db_diagnostic)
        db.commit()
        db.refresh(db_diagnostic)
        return db_diagnostic
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el diagnóstico") from e
    
@router.get('/diagnostic/patient/{id}')
def get_list(id: int, db: Session = Depends(get_db)):
    try:
        # Realizamos un JOIN entre Diagnostic y PatientDiagnostic
        resultado = (
            db.query(Diagnostic)
            .join(PatientDiagnostic, Diagnostic.id == PatientDiagnostic.diagnostic_id)
            .filter(PatientDiagnostic.patient_id == id)
            .all()
        )
        return resultado
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se encuentran datos") from e
