# importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

# Inicialización de API
app = FastAPI(
    title='Mi primer API',
    description='Andrés Martínez Badillo',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)