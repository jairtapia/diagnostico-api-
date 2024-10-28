from fastapi import APIRouter,Depends
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.routers.user.model.user import UserValidator, CredentialsValidator
from app.db.schemas.user import User, Credentials,UserType
'''
para crear una nueva ruta
importamos el modelo de la respuesta que es la clase de pydantic
ejemplo
from app.routers.users.model.userMd import UserValidator
y importamos la clase de la tabla que va a usar el orm
ejemplo
from app.routers.users.schema.userDb import User
fijate bien en las rutas deben estar bien
'''

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/Signin")
def save_credentials(credentials:CredentialsValidator,db: Session = Depends(get_db)):
    status = "bad"
    try:
        hashed_password = hash_password(credentials.password)
        # Convertir el modelo Pydantic a diccionario y pasarlo al modelo SQLAlchemy
        credentials_dict = credentials.dict()
        credentials_dict["password"] = hashed_password
        credentials_db = Credentials(**credentials_dict)
        # Agregar a la base de datos
        db.add(credentials_db)
        db.commit()
        db.refresh(credentials_db)
        # Si todo sale bien, cambiamos el estado a 'success'
        status = "success"
    except Exception as e:
        # Si hay un error, lanzamos una excepción o manejamos el error como prefieras
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al guardar las credenciales")
    return {'status': status, 'credentials': credentials_db}

@router.post("/Signin/data")
def save_data(user:UserValidator,db: Session = Depends(get_db)):
    status = 'bad'
    try:
        user_dict = user.dict(exclude_unset=True)
        user_dict.pop('user_id', None)
        user_db = User(**user_dict)
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        status = "ok"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=str(e))
    return {'registro status':status}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/Login",response_model=UserValidator)
def verify_user(credentials:CredentialsValidator, db: Session = Depends(get_db)):
    try:
        # Buscar las credenciales en la base de datos por email
        db_credentials = db.query(Credentials).filter(Credentials.email == credentials.email).first()
        if not db_credentials:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="invalid email",
            )
        # Verificar la contraseña hasheada
        if not verify_password(credentials.password,db_credentials.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Si la contraseña es válida, buscar el usuario asociado
        user = db.query(User).filter(User.user_id == db_credentials.credential_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        # Retornar el usuario si todo está correcto
        return user
    except HTTPException as e:
        # Rethrow de excepciones HTTP
        raise e
    except Exception as e:
        # Manejar cualquier otro error no previsto
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
    
@router.get("/User/find/{user_id}",response_model=UserValidator)
def findUser(id:int, db:Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el usuario") from e

@router.get("/User/find/name/{fname}",response_model=UserValidator)
def findUser(name:str, db:Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.user_name == name).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar el usuario") from e

@router.put("/User/edit/{user_id}",response_model=UserValidator)
def editUser(id:int, user:UserValidator, db :Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.user_id == id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        user_data = user.dict(exclude_unset=True)
        user_data.pop('user_id', None)  
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user  # Cambiado para retornar el objeto actualizado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al editar el usuario") from e

@router.delete("/User/delete/{user_id}")
def deleteUser(id:int, db:Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.user_id == id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(db_user)
        db.commit()
        return {"message": "Usuario eliminado con éxito"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el usuario") from e
    
@router.get('/users')
def GetUsers(db:Session = Depends(get_db)):
    users = db.query(User,UserType.user_type_name).join(UserType).all()
    users_list = [{
        'id': user.user_id,
        'nombre': user.user_name,
        'apellido': user.last_name_f,
        'apellido m': user.last_name_m,
        'telefono':user.telefono,
        'rol': user_type_name
    } for user,user_type_name  in users]
    return users_list


