from sqlalchemy import Column, SmallInteger, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserType(Base):
    __tablename__ = 'UserType'
    user_type_id = Column(SmallInteger, primary_key=True, index=True)
    user_type_name = Column(String(50), nullable=False)

class User(Base):
    __tablename__ = 'User'
    user_id = Column(SmallInteger, primary_key=True, index=True)
    user_name = Column(String(30), nullable=False)
    last_name_f = Column(String(30), nullable=True)
    last_name_m = Column(String(30), nullable=True)
    telefono = Column(String(10), nullable=False)  
    user_type = Column(SmallInteger, ForeignKey("UserType.user_type_id"), nullable=False)

class Credentials(Base):
    __tablename__ = 'Credentials'
    credential_id = Column(SmallInteger, primary_key=True, index=True)
    email = Column(String(30), nullable=False)
    password = Column(String(128), nullable=False)
