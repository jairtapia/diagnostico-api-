#aqui importamos las tablas que queremos crear
#ejemplo
# >>> from app.routers.users.schema.userDb import User, UserType
from app.db.schemas.user import User, UserType, Credentials
from app.db.schemas.patient import Patient
from app.db.schemas.appointment import ClinicRoom,ClinicRoomSchedule,Appointment
from app.db.schemas.Disease import Disease
from app.db.schemas.Sign import Sign, SignDisease
from app.db.schemas.Symptom import Symptom, SymptomDisease
from app.db.schemas.DiesaseTest import DiseaseTest,TestsDiseases
from app.db.schemas.Diagnostic import Diagnostic,PatientDiagnostic
from app.db.schemas.PostMorten import Postmorten
from app.db.database import engine, Base


#super importante primero crea la base de datos con el nombre que quieras y asignala a tu archivo .env

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    UserType.__table__.create(bind=engine)
    Credentials.__table__.create(bind=engine)
    User.__table__.create(bind=engine)
    Patient.__table__.create(bind=engine)
    ClinicRoom.__table__.create(bind=engine)
    ClinicRoomSchedule.__table__.create(bind=engine)
    Appointment.__table__.create(bind=engine)
    Sign.__table__.create(bind=engine)
    Symptom.__table__.create(bind=engine)
    Disease.__table__.create(bind=engine)
    SignDisease.__table__.create(bind=engine)
    SymptomDisease.__table__.create(bind=engine)
    DiseaseTest.__table__.create(bind=engine)
    TestsDiseases.__table__.create(bind=engine)
    Diagnostic.__table__.create(bind=engine)
    PatientDiagnostic.__table__.create(bind=engine)
    Postmorten.__table__.create(bind=engine)
    print("Tablas creadas exitosamente.")