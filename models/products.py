from pydantic import BaseModel, Field

class TipoProducto(BaseModel):
    nombre : str = Field(max_length=50)
    descripcion : str = Field(max_length=200)

class Etiqueta(BaseModel):
    nombre : str

class Producto(BaseModel):
    tienda : int
    nombreProducto : str = Field(max_length=100)
    descripcion : str = Field(max_length=200)
    imagien : str = Field(max_length=200)
    tipoProducto : int
    existencias : int 
    valorUnitario : float
