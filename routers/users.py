from fastapi import APIRouter,Form,Depends,HTTPException,status
from typing import Annotated
from models.user import User,UserDb
from database import get_db
from models.functions import authId,searchUser
from mysql.connector import Error
from const.encrypConst import ErrorConst
import bcrypt

router = APIRouter(
    prefix= "/users"
)


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user : UserDb):
    aux = searchUser()
    if aux is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="username already in use")
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(user.contrasenia,'utf-8'),sal),'utf-8')
        cursor = conection.cursor()
        cursor.execute(f"INSERT INTO usuario(usuario,contrasenia,emailRespaldo,nombreCompleto) VALUES('{user.usuario}','{password}','{user.emailRespaldo}','{user.nombreCompleto}');")
        conection.commit()
        return "user created"
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


@router.get("/user", status_code=status.HTTP_200_OK)
async def getUser(userId : str = Depends(authId)):
    
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


@router.put("/modify",status_code=status.HTTP_205_RESET_CONTENT)
async def modifyUser(user : User,userId : str = Depends(authId)):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET emailRespaldo = '{user.emailRespaldo}', nombreCompleto = '{user.nombreCompleto}',numeroTelefono = '{user.numeroTelefono}', direccion = '{user.direccion}' WHERE idUsuario = {userId}")
        conection.commit()
        return "user modified"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo "
    finally:
        conection.close()


@router.put("/changePass",status_code=status.HTTP_205_RESET_CONTENT)
async def changePass(passW : Annotated[str,Form()],userId : str = Depends(authId)):
    conection = get_db()
    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(passW,'utf-8'),sal),'utf-8')
        cursor = conection.cursor()
        cursor.execute(f"UPDATE usuario SET contrasenia = '{password}' WHERE idUsuario = {userId};")
        conection.commit()
        return "change successful"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo"
    finally:
        conection.close()


@router.delete("/deleteUser",status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(userId : str = Depends(authId)):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"DELETE FROM usuario WHERE idUsuario = {userId};")
        conection.commit()
        return "deleted successful"
    except Error:
        raise ErrorConst.executeSql
    except:
        return "fallo"
    finally:
        conection.close()





