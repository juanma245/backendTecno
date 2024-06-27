from pydantic import BaseModel, Field

class TipoProducto():
    nombre : str = Field(max_length=50)
    descripcion : str = Field(max_length=200)
