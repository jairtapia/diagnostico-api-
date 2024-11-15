from sqlalchemy import Column, SmallInteger, String, ForeignKey
from app.db.database import Base

class Diagnostic(Base):
    __tablename__ = 'Diagnostic'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    medico =  Column(SmallInteger, ForeignKey('User.user_id'), nullable=False)
    paciente =  Column(SmallInteger, ForeignKey('Patient.patient_id'), nullable=False)
    descripcion = Column(String(255), nullable=False)
    receta = Column(String(255), nullable=True)
    enfermedad = Column(SmallInteger, ForeignKey('Disease.id'), nullable=False)
    estado = Column(String(255), nullable=False)

class PatientDiagnostic(Base):
    __tablename__ = 'PatientDiagnostic'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(SmallInteger, ForeignKey('Patient.patient_id'), nullable=False)
    diagnostic_id = Column(SmallInteger, ForeignKey('Diagnostic.id'), nullable=False)


