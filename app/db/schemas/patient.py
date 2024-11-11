from sqlalchemy import Column, SmallInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Patient(Base):
    __tablename__='Patient'
    patient_id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    last_name_f = Column(String(30), nullable=True)
    last_name_m = Column(String(30), nullable=True)
    age = Column(SmallInteger, nullable=False)
    phone = Column(String(10), nullable=False)
    address = Column(String(30), nullable=False)
    state = Column(String(30), nullable=False)


