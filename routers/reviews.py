from fastapi import APIRouter,Depends,status,HTTPException
from models.functions import authId,existsStoreById
from models.review import usuarioValoraTienda
from const.encrypConst import ErrorConst
from database import get_db
from mysql.connector import Error

router = APIRouter(prefix="/reviews")

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

@router.post("/addReview", status_code=status.HTTP_201_CREATED)
async def addReview(review : usuarioValoraTienda, userID : str = Depends(authId)):
    if not existsStoreById(review.tienda):
        raise ErrorConst.storeDontExist
    
    if 0 > review < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="valoration out of range")

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
    