from fastapi import APIRouter,status,Depends,HTTPException,status
from models.products import TipoProducto,Etiqueta,Producto
from const.encrypConst import ErrorConst
from mysql.connector import Error
from database import get_db
from models.functions import authId,searchStore,getLevel,existsType,searchProduct,existsProduct
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
        return "Type created"    
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

@router.post("/addProduct/{storeName}",status_code=status.HTTP_201_CREATED)
async def addProduct(storeName : str, product : Producto, userID : str = Depends(authId)):
    if product.existencias < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="negative stock")
    
    if product.valorUnitario < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="negative price")
    idStore = searchStore(storeName)
    if idStore is None:
        raise ErrorConst.storeDontExist
    
    if existsProduct(product.nombreProducto,idStore[0]) == True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="product name already in use")
            

    level = getLevel(idStore[0],userID)
    if level is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user has not authorization")
    
    if existsType(product.tipoProducto) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product type doesn't exists")
    
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        INSERT INTO producto(tienda,nombreProducto,descripcion,imagen,tipoProducto,existencias,valorUnitario)
                        VALUES(%s,%s,%s,%s,%s,%s,%s)
                        """,(idStore[0],product.nombreProducto,product.descripcion,product.imagen,product.tipoProducto,product.existencias,product.valorUnitario))
        connection.commit()
        return "Product Created"    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/listProducts",status_code=status.HTTP_200_OK)
async def listProducs():
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT nombreProducto, descripcion, imagen, valorUnitario
                        FROM producto
                        """)
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/listProducts/{storeName}",status_code=status.HTTP_200_OK)
async def listProducs(storeName : str):
    idStore = searchStore(storeName)
    if idStore is None:
        raise ErrorConst.storeDontExist
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT nombreProducto, descripcion, imagen, valorUnitario
                        FROM producto
                        WHERE tienda = %s
                        """,(idStore[0],))
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/listProduct/{productName}",status_code=status.HTTP_200_OK)
async def listProduct(productName : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT nombreProducto, descripcion, imagen, valorUnitario
                        FROM producto
                        WHERE nombreProducto = %s
                        """,(productName,))
        register = cursor.fetchall()
        if register is None:
            return "store doesn't exists"
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.get("/product/{idProduct}",status_code=status.HTTP_200_OK)
async def getProduc(idProduct : str):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT p.nombreProducto, t.nombreTienda, p.descripcion, p.imagen,tp.nombre, p.tipoProducto, p.existencias, p.valorUnitario
                        FROM producto as p
                        JOIN tienda as t ON p.tienda = t.idTienda
                        JOIN tipoProducto as tp ON tp.idTipoProducto = p.tipoProducto
                        WHERE idProducto = %s
                        """,(idProduct,))
        register = cursor.fetchall()
        return register
    except Error as err:
        print(err)
        raise ErrorConst.executeSql
    finally:
        connection.close()