from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status


class const():
    ALGORITHM = "HS256"
    ACCESS_DURATION = 60
    SECRET = "a53506e6bfe66507482007c816d394c3f4873de276e1a02ad7a1d272e5f6e46129714d113e26b6cb071ea3a6adfdd2857e4b12d639fb95a5da08ff6a5155015c"
    oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

class dbConst():
    host = 'localhost'
    port = '3306'
    user = 'root'
    password = ''
    db = 'tiendaTecno'

class ErrorConst():
    executeSql = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="execute sql error")
    
    storeDontExist = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="store don't exists")
    
    userDontExist = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user don't exists")


