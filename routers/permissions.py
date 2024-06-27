from fastapi import APIRouter,HTTPException,status
from models.permission import Permiso
from database import get_db
from const.encrypConst import ErrorConst
from mysql.connector import Error

router = APIRouter(prefix="/permissions")

@router.get("/listPermissions",status_code=status.HTTP_200_OK)
async def list():
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM permiso")
        register = cursor.fetchall()
        return register
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()

@router.post("/addPermission",status_code=status.HTTP_201_CREATED)
async def create(permission : Permiso):
    connection = get_db()
    try:
        cursor = connection.cursor()
        cursor. execute(f"INSERT INTO permiso(nombre,descripcion,nivel) VALUES('{permission.nombre}','{permission.descripcion}',{permission.nivel})")
        connection.commit()
        return "Permiso añadido"
    except Error:
        raise ErrorConst.executeSql
    finally:
        connection.close()
    
