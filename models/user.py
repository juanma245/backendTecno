from pydantic import BaseModel, Field
from typing import Union

class User(BaseModel):
    idUsuario : int | None = None
    user : Union[str,None] = Field(min_length=4, max_length=50) and None
    email : str = Field(max_length=100) and None
    name : str = Field(max_length=100) and None
    phone : Union[str, None]= Field(max_length=12) and None
    image : Union[str, None] = Field(max_length=200) and None
    address : Union[str, None] = Field(max_length=100) and None

class UserDb(User):
    contrasenia : str = Field(max_length=500)
