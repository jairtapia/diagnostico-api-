from sqlalchemy import Column, SmallInteger, String, ForeignKey
from app.db.database import Base

class Postmorten(Base):
    __tablename__ = 'Postmorten'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    medico =  Column(SmallInteger, ForeignKey('User.user_id'), nullable=False)
    paciente =  Column(SmallInteger, ForeignKey('Patient.patient_id'), nullable=False)
    observaciones = Column(String(255), nullable=False)
    diagnostico = Column(SmallInteger, ForeignKey('Diagnostic.id'), nullable=False)
    fecha = Column(String(30), nullable=False)
    causa = Column(SmallInteger, ForeignKey('Disease.id'), nullable=False)
