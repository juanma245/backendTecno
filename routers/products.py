from fastapi import APIRouter,status
from models.products import TipoProducto
from const.encrypConst import ErrorConst
from mysql.connector import Error
from database import get_db

router = APIRouter(prefix="/products")

@router.post("/addType",status_code=status.HTTP_201_CREATED)
async def addType(type : TipoProducto):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO tipoProducto(nombre,descripcion) VALUES('{type.nombre}','{type.descripcion}');")
        connection.commit()
        return "Product created"    
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()
