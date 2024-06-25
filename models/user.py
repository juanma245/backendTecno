from pydantic import BaseModel, Field

class User(BaseModel):
    idUsuario : int | None = None
    usuario : str | None = Field(min_length=4, max_length=50) and None
    emailRespaldo : str = Field(max_length=100) and None
    nombreCompleto : str = Field(max_length=100) and None
    numeroTelefono : str | None= Field(max_length=12) and None
    imagen : str | None = Field(max_length=200) and None
    direccion : str | None = Field(max_length=100) and None

class UserDb(User):
    contrasenia : str = Field(max_length=500)
