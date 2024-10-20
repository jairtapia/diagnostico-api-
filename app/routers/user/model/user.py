from pydantic import BaseModel,EmailStr,Field
from datetime import date
from typing import Optional

class UserValidator(BaseModel):
    user_id: Optional[int] = None
    user_name: str 
    last_name_f: str 
    last_name_m: str 
    telefono: str
    user_type: int
    crd_id: int

    class Config:
        orm_mode = True

class CredentialsValidator(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length= 8)
    class Config():
        orm_mode = True

if __name__ =='__main__':
    import requests
    import json
    '''
    puedes crear tu usuario aqui si quieres
    rellena con tus datos o utiliza ese usuario
    primero activa el servidor de fast api
    '''
    user_credentials = CredentialsValidator(
        email="juan@gmail.com",
        password="1234567890"
    )

    response = requests.post("http://127.0.0.1:8000/Signin", json=user_credentials.dict())  
    if response.status_code == 200:
        users = response.json()
        print(json.dumps(users, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")
    
    '''
    generando guardando los datos usuario
    '''
    user_data = UserValidator(
        user_name="juan",
        last_name_f="perez",
        last_name_m="gomez",
        telefono="23453245",
        user_type=1,
        crd_id=1
    )
    response = requests.post("http://127.0.0.1:8000/Signin/data", json=user_data.dict())  
    if response.status_code == 200:
        users = response.json()
        print(json.dumps(users, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")