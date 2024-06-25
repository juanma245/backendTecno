from fastapi import APIRouter,Form,Depends
from typing import Annotated
from models.user import User,UserDb
from database import get_db
from models.functions import current_user
import bcrypt

router = APIRouter(
    prefix= "/users"
)

@router.get("/prueba")
async def me (user : str = Depends(current_user)):
 return user

@router.post("/register")
async def register(user : UserDb):
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(user.contrasenia,'utf-8'),sal),'utf-8')
        print("llega")
        cursor = conection.cursor()
        cursor.execute(f"INSERT INTO usuario(usuario,contrasenia,emailRespaldo,nombreCompleto) VALUES('{user.usuario}','{password}','{user.emailRespaldo}','{user.nombreCompleto}');")
        conection.commit()
        return "registro exitoso"
    except:
        return "fallo"
    finally:
        conection.close()


@router.get("/listUser")
async def listUser():
    conection = get_db()
    try:
        if(conection == "no se pudo "):
            return "algo fallo"
        else:
            cursor = conection.cursor()
            print("llega")
            cursor.execute("SELECT * FROM usuario")
            register = cursor.fetchall()
            return(register)
    except:
        return "fallo et je ne sais pas pourqoi"
    finally:
        conection.close()


@router.get("/user/{userId}")
async def getUser(userId : int):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT * FROM usuario WHERE idUsuario = {userId};")
        register = cursor.fetchone()
        return register
    except:
        return "fallo"
    finally:
        conection.close()


@router.put("/modify/{userId}")
async def modifyUser(user : User,userId : int):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET emailRespaldo = '{user.emailRespaldo}', nombreCompleto = '{user.nombreCompleto}',numeroTelefono = '{user.numeroTelefono}', direccion = '{user.direccion}' WHERE idUsuario = {userId}")
        conection.commit()
        return "Modificacion exitosa"
    except:
        return "fallo "
    finally:
        conection.close()


@router.put("/changePass/{userId}")
async def changePass(userId : int,passW : Annotated[str,Form()]):
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(passW,'utf-8'),sal),'utf-8')
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET contrasenia = '{password}' WHERE idUsuario = {userId};")
        conection.commit()
        return "Cambio exitoso"
    except:
        return "fallo"
    finally:
        conection.close()


@router.delete("/deleteUser/{userId}")
async def deleteUser(userId : int):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"DELETE FROM usuario WHERE idUsuario = {userId};")
        conection.commit()
        return "Eliminacion exitosa"
    except:
        return "fallo"
    finally:
        conection.close()





