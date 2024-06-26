from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


class const():
    ALGORITHM = "HS256"
    ACCESS_DURATION = 60
    SECRET = "a53506e6bfe66507482007c816d394c3f4873de276e1a02ad7a1d272e5f6e46129714d113e26b6cb071ea3a6adfdd2857e4b12d639fb95a5da08ff6a5155015c"
    oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

    


