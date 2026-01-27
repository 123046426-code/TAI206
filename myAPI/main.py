#importaciones
from fastapi import FastAPI

#Inicializacion
app= FastAPI()

#EndPoints
@app.get("/")
async def helloworld():
    return {"mensaje":"Hello World FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenido a tu API REST"}