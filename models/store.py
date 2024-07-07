from pydantic import BaseModel,Field

class Tienda(BaseModel):
    nombreTienda : str = Field(max_length=50)
    direccionFisica : str = Field(max_length=100)
    logo : str = Field(max_length=200)
    descripcion : str = Field(max_length=500)

class userAdminStore(BaseModel):
    user : str
    store : str
    level : int

class userAux(BaseModel):
    user : str
