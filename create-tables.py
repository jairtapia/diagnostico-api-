#aqui importamos las tablas que queremos creat
#ejemplo
# >>> from app.routers.users.schema.userDb import User, UserType
from app.db.schemas.user import User, UserType, Credentials
from app.db.database import engine, Base


#super importante primero crea la base de datos con el nombre que quieras y asignala a tu archivo .env

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")