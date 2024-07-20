from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.store import Tienda,userAdminStore,userAux
from database import executeChange,executeSelectAll,executeSelectOne
from const.encrypConst import ErrorConst
from models.functions import existsStore,searchStore,getLevel,searchUser,authId

router = APIRouter(prefix="/stores")


@router.post("/addStore",status_code=status.HTTP_201_CREATED)
async def addStore(store : Tienda, userId : str = Depends(authId)):
    if existsStore(store.nombreTienda):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Store already exists")
    sql1 = """
            INSERT INTO tienda(nombreTienda,direccionFisica,logo,descripcion) 
            VALUES(%s,%s,%s,%s)
        """
    datos1 = (store.nombreTienda,store.direccionFisica,store.logo,store.descripcion)
    
    executeChange(sql1,datos1)
    idStore = searchStore(store.nombreTienda)
    
    sql2 = """
                INSERT INTO usuarioAdministraTienda(usuario,tienda,permiso) 
                VALUES(%s,%s,1)
            """
    
    datos2 = (userId,idStore[0])

    executeChange(sql2,datos2)

    return JSONResponse(content={"message" : "Store created"})

@router.get("/listStores",status_code=status.HTTP_200_OK)
async def list():
    sql = """
            SELECT * 
            FROM tienda
        """
    register = executeSelectAll(sql,())

    responseList = []
    for store in register:
        response = {
            "id" : store[0],
            "name" : store[1],
            "address" : store[2],
            "logo" : store[3],
            "description" : store[4]
        }
        responseList.append(response)

    jresponse = jsonable_encoder(responseList)
    return JSONResponse(content=jresponse)
    
@router.get("/store/{storeName}",status_code=status.HTTP_200_OK)
async def getStore(storeName : str):
    if not existsStore(storeName):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="store don't exists")
    
    sql = """
            SELECT idTienda,direccionFisica,logo,descripcion 
            FROM tienda 
            WHERE nombreTienda = %s
        """
    
    datos = (storeName,)

    store = executeSelectOne(sql,datos)

    response = {
        "id" : store[0],
        "name" : storeName,
        "address" : store[1],
        "logo" : store[2],
        "description" : store[3]
    }

    jresponse = jsonable_encoder(response)

    return JSONResponse(content=jresponse)

@router.delete("/deleteStore/{storeName}",status_code=status.HTTP_200_OK)
async def delete(storeName : str):
    idStore = searchStore(storeName)
    if idStore is None:
        raise ErrorConst.storeDontExist
    sql = """
            DELETE FROM tienda
            WHERE idTienda = %s
        """
    
    datos = (idStore[0],)
    executeChange(sql,datos)
    return JSONResponse(content={"message" : "store deleted"})
    
@router.post("/addVendor", status_code=status.HTTP_200_OK)
async def addVendor(userAdd : userAdminStore, userID : str = Depends(authId)):
    idStore = searchStore(userAdd.store)
    if idStore is None:
        raise ErrorConst.storeDontExist
    level = getLevel(idStore[0],userID)
    if level is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user has not authorization")
    elif level != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user has not level enought for this function ")
    
    idUser = searchUser(userAdd.user)
    if idUser is None:
        raise ErrorConst.userDontExist
    sql = """
            INSERT INTO usuarioAdministraTienda(usuario,tienda,permiso) 
            VALUES(%s,%s,%s)
        """
    datos = (idUser[0],idStore[0],userAdd.level)

    executeChange(sql,datos)

    return JSONResponse(content={"message" : "added"})
    
@router.delete("/deleteVendor/{storeName}", status_code=status.HTTP_200_OK)
async def deleteVendor(storeName : str,user : userAux, userID : str = Depends(authId)):
    idStore = getStore(storeName)
    if(idStore is None):
        raise ErrorConst.storeDontExist
    idUser = searchUser(user)
    if(idUser is None):
        raise ErrorConst.userDontExist
    level = getLevel(idStore[0],userID)
    if level is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user has not authorization")
    elif level != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="user has not level enought for this function ")
    
    sql = """
            DELETE FROM usuarioAdministraTienda
            WHERE tienda = %s AND usuario = %s
        """
    
    datos = (idStore[0],idUser[0])

    executeChange(sql,datos)

    return JSONResponse(content={"message" : "vendor deleted"})

@router.get("/listVendor/{storeName}",status_code=status.HTTP_200_OK)
async def listVendor(storeName : str):
    idStore = searchStore(storeName)
    if idStore is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="store don't exists")
    sql = """
            SELECT udt.usuario, udt.permiso, u.usuario, u.nombreCompleto 
            FROM usuarioAdministraTienda as udt 
            JOIN usuario as u ON u.idUsuario = udt.usuario 
            WHERE tienda = %s
        """
    
    datos = (idStore[0],)

    vendors = executeSelectAll(sql,datos)

    responseList = []
    for vendor in vendors:
        response = {
            "id" : vendor[0],
            "level" : vendor[1],
            "user" : vendor[2],
            "name" : vendor[3]
        }
        responseList.append(response)

    jresponse = jsonable_encoder(responseList)

    return JSONResponse(content=jresponse)
    
    

    

    
    
    




    