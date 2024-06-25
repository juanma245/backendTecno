from fastapi import APIRouter,Form,Depends,HTTPException,status
from models.functions import searchUser
from typing import Annotated
from const.encrypConst import const
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

import bcrypt

router = APIRouter()

@router.get("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    try:
        register = searchUser(form.username)
        if register == "Not found":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
        
        if bcrypt.checkpw(form.password, register.contrasenia):
            return {"access_token" : register.usuario,"token_type" : "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="contraseña incorrecta")


        
    except Exception as ex:
        return ex