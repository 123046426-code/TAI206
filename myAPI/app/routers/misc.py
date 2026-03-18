from fastapi import APIRouter
import asyncio
from app.data.database import usuarios
from typing import Optional

router= APIRouter(
    tags=["Varios"]
)

# ----------- Inicio -----------

@router.get("/")
async def helloworld():
    return {"mensaje": "Hello world FastAPI"}

@router.get("/v1/bienvenidos")
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST"}

# ----------- Asincronía -----------

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(2)
    return {"mensaje": "Tu calificación en TAI es 10"}

# ----------- Parámetro obligatorio -----------

@router.get("/v1/parametro/{id}")
async def consulta_usuario(id: int):
    return {"usuario encontrado": id}

# ----------- Parámetro opcional -----------

@router.get("/v1/parametro_op/")
async def consulta_op(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario": usuario}
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"aviso": "No se proporcionó ID"}