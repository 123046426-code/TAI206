#uvicorn main:app --reload
#documentación /docs para usuario: /redoc

#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Inicializacion o instancia de la API
app= FastAPI(
    title='My first API',
    description='Andrés Martínez Badillo',
    version='1.0'
)

#diccionario
usuarios=[
    {"id":1,"nombre":"andy","edad":20},
    {"id":2,"nombre":"martin","edad":20},
    {"id":3,"nombre":"tovar","edad":21}
]

#EndPoints
@app.get("/", tags=['Inicio'])
async def helloworld():
    return {"mensaje":"Hello World FastAPI"}

@app.get("/welcome", tags=['Inicio'])
async def welcome():
    return {"mensaje":"Welcome to your API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"Tu calificacion en TAI es 10"}

#EndPoint con parametros obligatorios
@app.get("/v1/usuarios/{id}", tags=['Obligatorio'])
async def consultausuarios(id:int):
    await asyncio.sleep(5) #esta linea está de más
    return {"Usuario encontrado":id }

#EndPoint con parametros opcionales
@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaop(id: Optional[int]=None):
    await asyncio.sleep(5) #esta linea está de más
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return{"Usuario encontrado":id, "usuario":usuario}
            else:
                return {"Mensaje": "Usuario no encontrado" }
    else:
        return{"Aviso": "No se proporciono id"}    