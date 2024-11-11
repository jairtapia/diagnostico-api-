from sqlalchemy import Column, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Disease(Base):
    __tablename__ = 'Disease'  # Nombre en minúscula para SQLAlchemy por convención
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    peligro = Column(SmallInteger, nullable=True)


class DiseaseDetail(Base):
    __tablename__ = 'Disease_detail'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    disease_id = Column(SmallInteger, ForeignKey('Disease.id'), nullable=False)
    sintoma_id = Column(SmallInteger, ForeignKey('Symptom.id'), nullable=True)
    signo_id = Column(SmallInteger, ForeignKey('Sign.id'), nullable=True)
