# importaciones
from fastapi import FastAPI
from app.routers import usuarios
from app.routers import misc

# Inicialización de API
app = FastAPI(
    title='Mi primer API',
    description='Andrés Martínez Badillo',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)