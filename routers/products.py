from fastapi import APIRouter,status
from models.products import TipoProducto,Etiqueta
from const.encrypConst import ErrorConst
from mysql.connector import Error
from database import get_db
#from typing import Annotated

router = APIRouter(prefix="/products")

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
#funciones de administrador
@router.get("/listType",status_code=status.HTTP_200_OK)
async def listType():
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT * 
                       FROM tipoProducto
                       """)
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()


@router.post("/addType",status_code=status.HTTP_201_CREATED)
async def addType(type : TipoProducto):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       INSERT INTO tipoProducto(nombre,descripcion) 
                       VALUES(%s,%s);
                       """,(type.nombre,type.descripcion))
        connection.commit()
        return "Product created"    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/listTag",status_code=status.HTTP_200_OK)
async def listTag():
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT * 
                       FROM etiqueta
                       """)
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.post("/addTag",status_code=status.HTTP_201_CREATED)
async def addTag(etiqueta : Etiqueta):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       INSERT INTO etiqueta(nombre) 
                       VALUES(%s)
                       """,(etiqueta.nombre,))
        connection.commit()
        return "tag created"    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

