from fastapi import FastAPI
from app.routers.user import user
from app.routers.Patients import patients
from app.routers.appointments import appointment
from app.routers.Disease import disease
from app.routers.Signs import signs
from app.routers.Symptoms import symptoms
from app.routers.Diagnostico import Diagnostico
'''
importamos las rutas
ejemplo
from app.routers.users import user
'''



'''
no me ignores >:)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
importante pasos para que todo funcione de forma local
primero 
mentira primero las dependencias
crear la base de datos con el nombre que quieras
segundo
crea un archivo .env en la carpeta db de preferencia con los nombres de variables 
MYSQLUSER=[tu usuario]Ñ
MYSQLHOST=[localhost]
MYSQL_ROOT_PASSWORD=[tu contrasña]
MYSQL_DATABASE=[nombre de la base de datos]
MYSQLPORT=[tu puerto]
tercero
crear las tablas ve al archivo create-tables
y ejecutalo normalmente si ver un mensaje asi >>"Tablas creadas exitosamente."
ya tienes todo listo.
para eso ejecuta normalmente el archivo de create-tables
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
'''

app = FastAPI()


#este lo podemos considerar como el healthcheck para ver que si este disponible la api
@app.get("/")
def read_root():
    return {"status": 'ok'}


'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
ejemplo de como agregar las rutas
app.include_router(user.router)
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
'''
app.include_router(user.router)
app.include_router(patients.router)
app.include_router(appointment.router)
app.include_router(signs.router)
app.include_router(symptoms.router)
app.include_router(disease.router)
app.include_router(Diagnostico.router)



'''
-------------------------------------------------------------------------------
para correr este servidor de fastapi estando dentro de la carpeta app
ejecuta
fastapi dev main.py
de forma local podemos ir a la direccion
http://127.0.0.1:80000 para hacer pruebas
y para hacer pruebas de post, put  etc 
http://127.0.0.1:80000/docs
-------------------------------------------------------------------------------
'''