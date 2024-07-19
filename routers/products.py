from fastapi import APIRouter,status,Depends,HTTPException,status
from models.products import TipoProducto,Etiqueta,Producto
from const.encrypConst import ErrorConst
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database import executeSelectAll,executeChange,executeSelectOne
from models.functions import authId,searchStore,getLevel,existsType,existsProduct
#from typing import Annotated

router = APIRouter(prefix="/products")


#funciones de administrador
@router.get("/listType",status_code=status.HTTP_200_OK)
async def listType():
    sql = """
            SELECT * 
            FROM tipoProducto
        """
    register = executeSelectAll(sql,())
    responseList = []
    for type in register:
        response = {
            "id" : type[0],
            "name" : type[1],
            "description" : type[2]
        }
        responseList.append(response)
    
    jresponse = jsonable_encoder(responseList)
    return JSONResponse(content=jresponse)
    
@router.post("/addType",status_code=status.HTTP_201_CREATED)
async def addType(type : TipoProducto):
    sql = """
            INSERT INTO tipoProducto(nombre,descripcion) 
            VALUES(%s,%s);
        """
    datos = (type.nombre,type.descripcion)

    executeChange(sql,datos)
    return JSONResponse(content={"message" : "type created"})
    
@router.get("/listTag",status_code=status.HTTP_200_OK)
async def listTag():
    sql = """
            SELECT * 
            FROM etiqueta
        """
    register = executeSelectAll(sql,())
    responseList = []
    for tag in register:
        response = {
            "id" : tag[0],
            "name" : tag[1]
        }
        responseList.append(response)
    
    jresponse = jsonable_encoder(responseList)
    return JSONResponse(content=jresponse)
    
@router.post("/addTag",status_code=status.HTTP_201_CREATED)
async def addTag(etiqueta : Etiqueta):
    sql = """
            INSERT INTO etiqueta(nombre) 
            VALUES(%s)
        """
    datos = (etiqueta.nombre,)

    executeChange(sql, datos)

    return JSONResponse(content={"message" : "tag created"})
    
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
    
    sql = """
            INSERT INTO producto(tienda,nombreProducto,descripcion,imagen,tipoProducto,existencias,valorUnitario)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
    datos = (idStore[0],product.nombreProducto,product.descripcion,product.imagen,product.tipoProducto,product.existencias,product.valorUnitario)

    executeChange(sql, datos)

    return JSONResponse(content={"message" : "Product created"})
    
@router.get("/listProducts",status_code=status.HTTP_200_OK)
async def listProducs():
    sql = """
            SELECT idProducto,nombreProducto, descripcion, imagen, valorUnitario,existencias
            FROM producto
        """
    register = executeSelectAll(sql,())
    responseList = []
    for product in register:
        response = {"idProduct" : product[0], 
                "name" : product[1],
                "description" : product[2],
                "image" : product[3],
                "unitPrice" : product[4],
                "stock" : product[5]}
        responseList.append(response)

   
    jResponse = jsonable_encoder(responseList)
    return JSONResponse(content=jResponse)
    
@router.get("/listProducts/{storeName}",status_code=status.HTTP_200_OK)
async def listProducs(storeName : str):
    idStore = searchStore(storeName)
    if idStore is None:
        raise ErrorConst.storeDontExist
    
    sql = """
            SELECT idProducto, nombreProducto, descripcion, imagen, valorUnitario,existencias
            FROM producto
            WHERE tienda = %s
        """
    datos = (idStore[0],)

    register = executeSelectOne(sql,datos)

    responseList = []
    for product in register:
        response = {"idProduct" : product[0], 
                "name" : product[1],
                "description" : product[2],
                "image" : product[3],
                "unitPrice" : product[4],
                "stock" : product[5]}
        responseList.append(response)
    
    jresponse = jsonable_encoder(responseList)
    return JSONResponse(content=jresponse)
    
@router.get("/listProduct/{productName}",status_code=status.HTTP_200_OK)
async def listProduct(productName : str):

    sql = """
            SELECT idProducto, nombreProducto, descripcion, imagen, valorUnitario
            FROM producto
            WHERE nombreProducto = %s
        """
    datos = (productName,)

    register = executeSelectAll(sql,datos)

    responseList = []
    for product in register:
        response = {"idProduct" : product[0], 
                "name" : product[1],
                "description" : product[2],
                "image" : product[3],
                "unitPrice" : product[4],
                "stock" : product[5]}
        
        responseList.append(response)
    
    jresponse = jsonable_encoder(responseList)
    return JSONResponse(content=jresponse)
    
@router.get("/product/{idProduct}",status_code=status.HTTP_200_OK)
async def getProduc(idProduct : str):
    sql = """
            SELECT p.nombreProducto, t.nombreTienda, p.descripcion, p.imagen,tp.nombre, p.existencias, p.valorUnitario
            FROM producto as p
            JOIN tienda as t ON p.tienda = t.idTienda
            JOIN tipoProducto as tp ON tp.idTipoProducto = p.tipoProducto
            WHERE idProducto = %s
        """
    datos = (idProduct,)

    register = executeSelectAll(sql,datos)

    response = {
        "id" : idProduct,
        "productName" : register[0],
        "storeName" : register[1],
        "description" : register[2],
        "image" : register[3],
        "typeName" : register[4],
        "stock" : register[5],
        "unitPrice" : register[6]
    }

    jresponse = jsonable_encoder(response)

    return JSONResponse(content=jresponse)
    