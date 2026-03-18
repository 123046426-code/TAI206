from pydantic import BaseModel, Field

#Modelo de validacion Pydantic

class UsuarioBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example="22")
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Martín")
    edad:int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121", example="87")