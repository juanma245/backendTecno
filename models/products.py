from pydantic import BaseModel, Field

class TipoProducto(BaseModel):
    nombre : str = Field(max_length=50)
    descripcion : str = Field(max_length=200)

class Etiqueta(BaseModel):
    nombre : str
