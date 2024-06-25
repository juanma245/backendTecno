from database import get_db
from fastapi import Depends,HTTPException,status
from const.encrypConst import const

def searchUser(username : str):
    conection = get_db()
    try:
        cursor = conection.cursor()
        cursor.execute(f"SELECT usuario, contrasenia FROM usuario WHERE usuario = '{username}';")
        register = cursor.fetchone()
        if register is None:
            return "Not found"
        return register
    except Exception as ex:
        return ex
    finally:
        conection.close()

async def current_user(token : str = Depends(const.oauth2)):
    register = searchUser(token)
    if register == "Not found":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no se encuantra autorizado ")
    return register.usuario
