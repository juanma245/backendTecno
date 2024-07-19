from fastapi import APIRouter,Form,Depends,HTTPException,status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Annotated
from models.user import User,UserDb
from database import executeChange,executeSelectAll,executeSelectOne
from models.functions import authId,existsUser
import bcrypt

router = APIRouter(
    prefix= "/users"
)


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user : UserDb):
    if existsUser(user.usuario):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="username already in use")

    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(user.contrasenia,'utf-8'),sal),'utf-8')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "encryp failed")
    
    sql = """
            INSERT INTO usuario(usuario,contrasenia,emailRespaldo,nombreCompleto) 
            VALUES(%s,%s,%s,%s);
        """
    
    datos = (user.usuario,password,user.emailRespaldo,user.nombreCompleto)

    executeChange(sql,datos)

    return "userCreated"

@router.get("/listUser")
async def listUser():
    
    sql = """
            SELECT * 
            FROM usuario
        """

    register = executeSelectAll(sql,())

    return register
    
@router.get("/user/{user}", status_code=status.HTTP_200_OK)
async def getUser(user : str):

    sql = """
            SELECT usuario,emailRespaldo,nombreCompleto,numeroTelefono,direccion 
            FROM usuario 
            WHERE usuario = %s
        """
    datos = (user,)

    register = executeSelectOne(sql,datos)

    return register
    
@router.get("/user", status_code=status.HTTP_200_OK)
async def getUser(userId : str = Depends(authId)):
    
    sql = """
            SELECT usuario,emailRespaldo,nombreCompleto,numeroTelefono,direccion 
            FROM usuario 
            WHERE idUsuario = %s
        """
    
    datos = (userId,)

    register = executeSelectOne(sql,datos)

    response = {"idUser" : userId, 
                "user" : register[0],
                "email" : register[1],
                "name" : register[2],
                "cell" : register[3],
                "address" : register[4]
                }   
    
    jResponse = jsonable_encoder(response)
    return JSONResponse(content=jResponse)
    
@router.put("/modify",status_code=status.HTTP_205_RESET_CONTENT)
async def modifyUser(user : User,userId : str = Depends(authId)):
    sql = """
            UPDATE usuario 
            SET emailRespaldo = %s, nombreCompleto = %s,numeroTelefono = %s, direccion = %s 
            WHERE idUsuario = %s
        """
    datos = (user.emailRespaldo,user.nombreCompleto,user.numeroTelefono,user.direccion,userId)

    executeChange(sql,datos)

    return "user modified"
    
@router.put("/changePass",status_code=status.HTTP_205_RESET_CONTENT)
async def changePass(passW : Annotated[str,Form()],userId : str = Depends(authId)):

    try:
        sal = bcrypt.gensalt()
        password = str(bcrypt.hashpw(bytes(passW,'utf-8'),sal),'utf-8')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail= "encryp failed")
    
    sql = """
            UPDATE usuario 
            SET contrasenia = %s 
            WHERE idUsuario = %s;
        """
    datos = (password,userId)

    executeChange(sql,datos)

    return "change successful"
    
@router.delete("/deleteUser",status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(userId : str = Depends(authId)):
    sql = """
            DELETE FROM usuario 
            WHERE idUsuario = %s;
        """
    datos = (userId,)

    executeChange(sql,datos)

    return "deleted successful"
    





