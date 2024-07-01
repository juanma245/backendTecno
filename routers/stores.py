from fastapi import APIRouter,status,HTTPException,Depends
from models.store import Tienda
from database import get_db
from const.encrypConst import ErrorConst
from mysql.connector import Error
from models.functions import existsStore,searchStore,authId

router = APIRouter(prefix="/stores")

'''
    plantilla 

    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"insertar sql")
        connection.commit()
        return ""    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"insertar sql")
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

'''

@router.post("/addStore",status_code=status.HTTP_201_CREATED)
async def addStore(store : Tienda, userId : str = Depends(authId)):
    connection = get_db()
    if existsStore(store.nombreTienda):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Store already exists")
    try:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO tienda(nombreTienda,direccionFisica,logo,descripcion) VALUES('{store.nombreTienda}','{store.direccionFisica}','{store.logo}','{store.descripcion}')")
        connection.commit()
        idStore = searchStore(store.nombreTienda)
        cursor.execute(f"INSERT INTO usuarioAdministraTienda(usuario,tienda,permiso) VALUES({userId},{idStore},1)")
        connection.commit()
        return "store created"    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/listStores",status_code=status.HTTP_200_OK)
async def list():
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM tienda")
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()


@router.get("/store/{storeName}",status_code=status.HTTP_200_OK)
async def getStore(storeName : str):
    if not existsStore(storeName):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="store don't exists")
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT nombreTienda,direccionFisica,logo,descripcion FROM tienda WHERE nombreTienda = '{storeName}'")
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

'''
@router.put("/addVendor/{storeName}", status_code=status.HTTP_200_OK)
async def addVendor(storeName : str, userID : str = Depends(authId)):
    idStore = searchStore(storeName)
    if idStore is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="store don't exists")
'''



    