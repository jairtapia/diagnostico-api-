from app.routers.user.model.user import UserValidator,CredentialsValidator
import requests
import json

def crearUser(crd,data):
    saveCredentials(crd)
    saveUser(data)

def saveUser(user_data):
    response = requests.post("http://127.0.0.1:8000/Signin/data", json=user_data.dict())  
    if response.status_code == 200:
        users = response.json()
        print(json.dumps(users, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")

def saveCredentials(user_credentials):
    response = requests.post("http://127.0.0.1:8000/Signin", json=user_credentials.dict())  
    if response.status_code == 200:
        users = response.json()
        print(json.dumps(users, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")

def editUser(id,data):
    response = requests.put(f"http://127.0.0.1:8000/User/edit/user_id?id={id}",json=data.dict())
    if response.status_code == 200:
        users = response.json()
        print(json.dumps(users, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")

def deleteUser(id):
    response = requests.delete(f"http://127.0.0.1:8000/User/delete/user_id?id={id}")
    if response.status_code == 200:
        user = response.json()
        print(json.dumps(user, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")

def searchUser(id):
    response = requests.get(f"http://127.0.0.1:8000/User/find/user_id?id={id}")
    if response.status_code == 200:
        user = response.json()
        print(json.dumps(user, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")

def searchByName(name):
    response = requests.get(f"http://127.0.0.1:8000/User/find/name/fname?name={name}")
    if response.status_code == 200:
        user = response.json()
        print(json.dumps(user, ensure_ascii=False, indent=4))
    else:
        print(f"Error al realizar la petición: {response.status_code}")


if __name__ == '__main__':
    user_credentials = CredentialsValidator(
        email="juan@gmail.com",
        password="1234567890"
    )
    user_data = UserValidator(
        user_name="juan",
        last_name_f="perez",
        last_name_m="gomez",
        telefono="23453245",
        user_type=1,
        crd_id=1
    )
    #crearUser(user_credentials,user_data)
    #searchUser(1)
    #searchByName('juan') 
    user_newData = UserValidator(
        user_name="daniela",
        last_name_f="perez",
        last_name_m="martinez",
        telefono="65763442",
        user_type=1,
        crd_id=1
    )
    #editUser(1,user_newData)
    #deleteUser(1)

