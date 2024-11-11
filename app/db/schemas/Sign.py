from sqlalchemy import Column, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Sign(Base):
    __tablename__ = 'Sign'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    descripcion = Column(String(2550), nullable=True)


class SignDisease(Base):
    __tablename__ = 'sign_disease'
    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    disease_id = Column(SmallInteger, ForeignKey('Disease.id'))
    sign_id = Column(SmallInteger, ForeignKey('Sign.id'))
