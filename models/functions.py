'''funciones de la api'''
from typing import Annotated
import jwt
from fastapi import Depends,HTTPException,status
from jwt.exceptions import InvalidTokenError
from mysql.connector import Error
from database import get_db
from const.encrypConst import const,ErrorConst


def searchUserDB(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT idUsuario, usuario, contrasenia FROM usuario WHERE usuario = '{username}';")
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error") from exc
    finally:
        conection.close()

def existsUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT idUsuario FROM usuario WHERE usuario = '{username}';")
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error") from exc
    finally:
        conection.close()

def existsStore(storeName : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT idTienda FROM tienda WHERE nombreTienda = '{storeName}'")
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

def searchStore(storeName : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT idTienda FROM tienda WHERE nombreTienda = '{storeName}'")
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()


async def authId(token : Annotated[str,Depends(const.oauth2)]):
    exepction = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credencials")
    try:
        payload = jwt.decode(token,const.SECRET,algorithms=[const.ALGORITHM])
        id : str = payload.get("sub")
        if id is None:
            raise exepction
    except InvalidTokenError:
        raise exepction

    return id
