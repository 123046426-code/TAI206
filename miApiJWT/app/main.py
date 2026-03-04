# importaciones
from fastapi import FastAPI, HTTPException, Depends, status
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Inicialización de API
app = FastAPI(
    title='Mi primer API con JWT',
    description='Andrés Martínez Badillo',
    version='1.0'
)

# BD ficticia
usuarios = [
    {"id": 1, "nombre": "Martin", "edad": 20},
    {"id": 2, "nombre": "Tovar", "edad": 21},
    {"id": 3, "nombre": "Rubio", "edad": 19},
]

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example="22")
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Martín")
    edad:int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121", example="87")

#Seguridad con HTTP Basic

security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username, "admin")
    contraAuth= secrets.compare_digest(credentials.password, "12345678")

    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )
    return credentials.username

# ----------- Inicio -----------

@app.get("/", tags=['Inicio'])
async def helloworld():
    return {"mensaje": "Hello world FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST"}

# ----------- Asincronía -----------

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(2)
    return {"mensaje": "Tu calificación en TAI es 10"}

# ----------- Parámetro obligatorio -----------

@app.get("/v1/parametro/{id}", tags=['Parametro Obligatorio'])
async def consulta_usuario(id: int):
    return {"usuario encontrado": id}

# ----------- Parámetro opcional -----------

@app.get("/v1/parametro_op/", tags=['Parametro Opcional'])
async def consulta_op(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"aviso": "No se proporcionó ID"}

# ----------- CRUD Usuarios -----------

# Obtener usuarios
@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def obtener_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# Obtener por ID
@app.get("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def obtener_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return usr

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# Crear usuario
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuario(usuario: UsuarioBase):

    if "id" not in usuario or "nombre" not in usuario or "edad" not in usuario:
        raise HTTPException(
            status_code=400,
            detail="Datos incompletos"
        )

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario)

    return {
        "mensaje": "Usuario agregado",
        "datos": usuario
    }

# Actualizar usuario
@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado",
                "datos": usuario_actualizado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# Eliminar usuario
@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth:str= Depends(verificar_Peticion)):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado",
                "datos": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no existe"
    )
