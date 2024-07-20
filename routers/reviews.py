from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from models.functions import authId,existsStoreById,existsProductById
from models.review import usuarioValoraTienda,usuarioValoraProducto
from const.encrypConst import ErrorConst
from database import executeChange

router = APIRouter(prefix="/reviews")

@router.post("/addReviewStore", status_code=status.HTTP_201_CREATED)
async def addReviewStore(review : usuarioValoraTienda, userID : str = Depends(authId)):
    if not existsStoreById(review.tienda):
        raise ErrorConst.storeDontExist
    
    if 0 > review.valoracion < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="valoration out of range")

    sql = """
            INSERT INTO usuarioValoraTienda(idUsuario,idTienda,valoracion,titulo,descripcion)
            VALUES(%s,%s,%s,%s,%s)
        """
    datos = (userID,review.tienda,review.valoracion,review.titulo,review.descripcion)

    executeChange(sql,datos)

    return JSONResponse(content={"message" : "review sended"})
    
@router.post("/addReviewProduct",status_code=status.HTTP_201_CREATED)
async def addReviewProduct(review : usuarioValoraProducto,userID = Depends(authId)):
    if not existsProductById(review.producto):
        raise ErrorConst.storeDontExist
    
    if 0 > review.valoracion < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="valoration out of range")

    sql = """
            INSERT INTO usuarioValoraProducto(idUsuario,idProducto,valoracion,titulo,descripcion)
            VALUES(%s,%s,%s,%s,%s)
        """
    datos = (userID,review.producto,review.valoracion,review.titulo,review.descripcion)

    executeChange(sql,datos)

    return JSONResponse(content={"message" : "review sended"})