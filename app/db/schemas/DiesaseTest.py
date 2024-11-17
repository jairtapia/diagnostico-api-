from sqlalchemy import Column, SmallInteger, String, ForeignKey
from app.db.database import Base

class Test(Base):
    __tablename__ = 'Test'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    nombre_prueba = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)

class TestsDiseases(Base):
    __tablename__ = 'TestsDiseases'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    id_disease_test = Column(SmallInteger,  ForeignKey('Test.id'),nullable=False,)
    id_disease = Column(SmallInteger, ForeignKey('Disease.id'),nullable=False)
