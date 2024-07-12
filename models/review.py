from pydantic import BaseModel

class usuarioValora(BaseModel):
    valoracion : int
    titulo : str | None = None
    descripcion : str | None = None

class usuarioValoraTienda(usuarioValora):
    tienda : int


class usuarioValoraProducto(usuarioValora):
    producto : int