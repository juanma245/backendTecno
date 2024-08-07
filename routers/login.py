import jwt
from fastapi import APIRouter,Depends,HTTPException,status
from models.functions import searchUserDB
from const.encrypConst import const
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta,timezone

import bcrypt

router = APIRouter()

@router.post("/login",status_code=status.HTTP_202_ACCEPTED)
async def login(form : OAuth2PasswordRequestForm = Depends()):
    register = searchUserDB(form.username)
    if register is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="incorrect user or password")

    
    if bcrypt.checkpw(bytes(form.password,'utf-8'),bytes(register[2],'utf-8')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="incorrect user or password")
    
    tokenExpiration = datetime.now(timezone.utc)+ timedelta(minutes=const.ACCESS_DURATION)
    
    accessToken = {
        "sub" : str(register[0]),
        "exp" : tokenExpiration
    }

    return {"access_token" : jwt.encode(accessToken,const.SECRET, algorithm=const.ALGORITHM),"token_type" : "bearer"}
        
   


        
        