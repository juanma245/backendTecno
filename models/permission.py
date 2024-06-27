from pydantic import BaseModel, Field

class Permiso(BaseModel):
    nombre : str 
    descripcion : str
    nivel : int