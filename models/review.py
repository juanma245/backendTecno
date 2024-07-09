from pydantic import BaseModel

class usuarioValoraTienda(BaseModel):
    tienda : int
    valoracion : int
    titulo : str | None = None
    descripcion : str | None = None