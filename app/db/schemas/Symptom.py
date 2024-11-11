from sqlalchemy import Column, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Symptom(Base):
    __tablename__ = 'Symptom'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)


class SymptomDisease(Base):
    __tablename__ = 'SymptomDisease'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    disease_id = Column(SmallInteger, ForeignKey('Disease.id'))
    symptom_id = Column(SmallInteger, ForeignKey('Symptom.id'))

