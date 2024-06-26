from database import get_db
from fastapi import Depends,HTTPException,status
from const.encrypConst import const
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Annotated

def searchUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT idUsuario, usuario, contrasenia FROM usuario WHERE usuario = '{username}';")
        register = cursor.fetchone()
        if register is None:
            return "Not found"
        return register
    except Exception as ex:
        return ex
    finally:
        conection.close()


async def authId(token : Annotated[str,Depends(const.oauth2)]):
    try:
        payload = jwt.decode(token,const.SECRET,algorithms=[const.ALGORITHM])
        id : str = payload.get("sub")
        if id is None:
            print("here")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="nope")
    except JWTError as jw:
        print(token)
        return jw

    return id
    