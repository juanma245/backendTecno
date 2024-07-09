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
        cursor.execute("""
                       SELECT idUsuario, usuario, contrasenia 
                       FROM usuario 
                       WHERE usuario = %s;
                       """,(username,))
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error as exc:
        print(exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error") from exc
    finally:
        conection.close()

def existsUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute("""
                       SELECT idUsuario 
                       FROM usuario 
                       WHERE usuario = %s;
                       """,(username,))
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error") from exc
    finally:
        conection.close()

def searchUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute("""
                       SELECT idUsuario 
                       FROM usuario 
                       WHERE usuario = %s;
                       """,(username,))
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error") from exc
    finally:
        conection.close()

def existsStore(storeName : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT idTienda 
                       FROM tienda 
                       WHERE nombreTienda = %s
                       """,(storeName,))
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

def existsStoreById(storeId : int):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT idTienda 
                       FROM tienda 
                       WHERE idTienda = %s
                       """,(storeId,))
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
        print(type(storeName))
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT idTienda 
                       FROM tienda 
                       WHERE nombreTienda = %s
                       """,(storeName,))
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error as er:
        print(er)
        raise ErrorConst.executeSql
    finally:
        connection.close()

def existsProduct(productName : str, idStore : int):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT idProducto
                       FROM producto
                       WHERE nombreProducto = %s AND tienda = %s
                        """,(productName,idStore))
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error as er:
        print (er)
        raise ErrorConst.executeSql
    finally:
        connection.close()

def searchProduct(productName : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT idProducto
                       FROM producto
                       WHERE nombreProducto = %s
                       """,(productName,))
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

def getLevel(idStore : int,idUser : int):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute("""
                       SELECT permiso 
                       FROM usuarioAdministraTienda 
                       WHERE usuario = %s AND tienda = %s;
                       """,(idUser,idStore))
        register = cursor.fetchone()
        if register is None:
            return False
        return True
    except Error as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="sql error") from exc
    finally:
        conection.close()

def existsType(idType : int):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT nombre 
                       FROM tipoProducto
                       WHERE idTipoProducto = %s
                       """,(idType,))
        register = cursor.fetchone()
        if register is None: 
            return False
        return True
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
