from sqlalchemy import Column, SmallInteger, String
from app.db.database import Base

class DiseaseTest(Base):
    __tablename__ = 'DiseaseTest'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    nombre_prueba = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)


class TestsDiseases(Base):
    __tablename__ = 'TestsDiseases'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    id_disease_test = Column(SmallInteger, nullable=False, foreign_key='DiseaseTest.id')
    id_disease = Column(SmallInteger, nullable=False, foreign_key='Disease.id')