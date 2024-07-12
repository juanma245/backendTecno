from fastapi import APIRouter,status
from models.permission import Permiso
from database import executeSelectAll,executeChange


router = APIRouter(prefix="/permissions")

@router.get("/listPermissions",status_code=status.HTTP_200_OK)
async def list():
    sql = """
            SELECT * 
            FROM permiso
        """
    register = executeSelectAll(sql,())
    return register
    
@router.post("/addPermission",status_code=status.HTTP_201_CREATED)
async def create(permission : Permiso):
    sql = """
            INSERT INTO permiso(nombre,descripcion,nivel) 
            VALUES(%s,%s,%s)
        """
    datos = (permission.nombre,permission.descripcion,permission.nivel)
    
    executeChange(sql,datos)
    return "permission created"
    
    
