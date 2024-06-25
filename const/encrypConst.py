from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


class const():
    ALGORITHM = "HS256"
    ACCESS_DURATION = 60
    SECRET = "7acdfa8ad391517ccf8ccff80a19674dS"
    oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

    


