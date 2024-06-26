from fastapi import APIRouter,Depends,HTTPException,status
from models.functions import searchUser
from const.encrypConst import const
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta,timezone

import bcrypt

router = APIRouter()

@router.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):

    register = searchUser(form.username)
    if register == "Not found":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    if bcrypt.checkpw(bytes(form.password,'utf-8'),bytes(register[2],'utf-8')):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="contraseña incorrecta")
    
    tokenExpiration = datetime.now(timezone.utc)+ timedelta(minutes=const.ACCESS_DURATION)
    

    print(type(register[0]))
    accessToken = {
        "sub" : str(register[0]),
        "exp" : tokenExpiration
    }

    return {"access_token" : jwt.encode(accessToken,const.SECRET, algorithm=const.ALGORITHM),"token_type" : "bearer"}
        
   


        
        