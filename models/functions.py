'''funciones de la api'''
from typing import Annotated
import jwt
from fastapi import Depends,HTTPException,status
from jwt.exceptions import InvalidTokenError
from database import executeSelectOne
from const.encrypConst import const


def searchUserDB(username : str):

    sql = """
                       SELECT idUsuario, usuario, contrasenia 
                       FROM usuario 
                       WHERE usuario = %s;
                       """
    datos = (username,)

    register = executeSelectOne(sql,datos)

    return register

def existsUser(username : str):
    sql = """
                       SELECT idUsuario 
                       FROM usuario 
                       WHERE usuario = %s;
                       """
    datos = (username,)

    register = executeSelectOne(sql,datos)

    if register is None:
        return False
    return True
    
def searchUser(username : str):
    sql = """
            SELECT idUsuario 
            FROM usuario 
            WHERE usuario = %s;
        """
    datos = (username,)

    register = executeSelectOne(sql,datos)

    return register
    
def existsStore(storeName : str):
    sql = """
            SELECT idTienda 
            FROM tienda 
            WHERE nombreTienda = %s
        """
    datos = (storeName,)

    register = executeSelectOne(sql,datos)

    if register is None:
        return False
    return True

def existsStoreById(storeId : int):
    sql = """
            SELECT idTienda 
            FROM tienda 
            WHERE idTienda = %s
        """
    datos = (storeId,)

    register = executeSelectOne(sql,datos)
    if register is None:
        return False
    return True
    
def searchStore(storeName : str):
    sql = """
            SELECT idTienda 
            FROM tienda 
            WHERE nombreTienda = %s
        """
    datos = (storeName,)

    register = executeSelectOne(sql,datos)

    return register
    
def existsProduct(productName : str, idStore : int):
    sql = """
            SELECT idProducto
            FROM producto
            WHERE nombreProducto = %s AND tienda = %s
        """
    datos = (productName,idStore)

    register = executeSelectOne(sql,datos)

    return register

def existsProductById(productId : int):
    sql = """
            SELECT idProducto
            FROM producto
            WHERE idProducto = %s
        """
    datos = (productId,)

    register = executeSelectOne(sql,datos)

    if register is None:
        return False
    return True

def searchProduct(productName : str):
    sql = """
            SELECT idProducto
            FROM producto
            WHERE nombreProducto = %s
        """
    
    datos = (productName,)

    register = executeSelectOne(sql,datos)

    return register
    
def getLevel(idStore : int,idUser : int):
    sql = """
            SELECT permiso 
            FROM usuarioAdministraTienda 
            WHERE usuario = %s AND tienda = %s;
        """
    datos = (idUser,idStore)

    register = executeSelectOne(sql,datos)

    return register

def existsType(idType : int):
    sql = """
            SELECT nombre 
            FROM tipoProducto
            WHERE idTipoProducto = %s
        """
    datos = (idType,)

    register = executeSelectOne(sql,datos)

    if register is None:
        return False
    return True
    
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
