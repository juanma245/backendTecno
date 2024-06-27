from fastapi import APIRouter,Form,Depends
from typing import Annotated
from models.user import User,UserDb
from database import get_db
from models.functions import authId
from mysql.connector import Error
from const.encrypConst import ErrorConst
import bcrypt

router = APIRouter(
    prefix= "/users"
)


@router.post("/register")
async def register(user : UserDb):
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(user.contrasenia,'utf-8'),sal),'utf-8')
        cursor = conection.cursor()
        cursor.execute(f"INSERT INTO usuario(usuario,contrasenia,emailRespaldo,nombreCompleto) VALUES('{user.usuario}','{password}','{user.emailRespaldo}','{user.nombreCompleto}');")
        conection.commit()
        return "registro exitoso"
    except Error:
        raise ErrorConst.executeSql
    finally:
        conection.close()


@router.get("/listUser")
async def listUser():
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute("SELECT * FROM usuario")
        register = cursor.fetchall()
        return(register)
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo et je ne sais pas pourqoi"
    finally:
        conection.close()


@router.get("/user")
async def getUser(userId : str = Depends(authId)):
    if userId is None:
        return "no autorizado "
    
    conection = get_db()
  
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT * FROM usuario WHERE idUsuario = {userId};")
        register = cursor.fetchone()
        return register
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo"
    finally:
        conection.close()


@router.put("/modify")
async def modifyUser(user : User,userId : str = Depends(authId)):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET emailRespaldo = '{user.emailRespaldo}', nombreCompleto = '{user.nombreCompleto}',numeroTelefono = '{user.numeroTelefono}', direccion = '{user.direccion}' WHERE idUsuario = {userId}")
        conection.commit()
        return "Modificacion exitosa"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo "
    finally:
        conection.close()


@router.put("/changePass")
async def changePass(passW : Annotated[str,Form()],userId : str = Depends(authId)):
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(passW,'utf-8'),sal),'utf-8')
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET contrasenia = '{password}' WHERE idUsuario = {userId};")
        conection.commit()
        return "Cambio exitoso"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo"
    finally:
        conection.close()


@router.delete("/deleteUser")
async def deleteUser(userId : str = Depends(authId)):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"DELETE FROM usuario WHERE idUsuario = {userId};")
        conection.commit()
        return "Eliminacion exitosa"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo"
    finally:
        conection.close()





