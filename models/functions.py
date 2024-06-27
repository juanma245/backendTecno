import jwt
from database import get_db
from fastapi import Depends,HTTPException,status
from jwt.exceptions import InvalidTokenError
from const.encrypConst import const
from typing import Annotated
from mysql.connector import Error




def searchUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT idUsuario, usuario, contrasenia FROM usuario WHERE usuario = '{username}';")
        register = cursor.fetchone()
        if register is None:
            return None
        return register
    except Error :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error")
    finally:
        conection.close()


async def authId(token : Annotated[str,Depends(const.oauth2)]):
    exepction = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credencials")
    try:
        payload = jwt.decode(token,const.SECRET,algorithms=[const.ALGORITHM])
        id : str = payload.get("sub")
        if id is None:
            raise exepction
    except InvalidTokenError:
        raise exepction

    return id
    