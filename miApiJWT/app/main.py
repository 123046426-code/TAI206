# importaciones
from fastapi import FastAPI, HTTPException, Depends, status 
import asyncio 
from typing import Optional 
from pydantic import BaseModel, Field 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import JWTError, jwt 
from passlib.context import CryptContext 
from datetime import datetime, timedelta 

# Inicialización de API
app = FastAPI(
    title='Mi primer API con JWT',
    description='Andrés Martínez Badillo',
    version='1.0'
)

# Hashing de contraseñas 
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de datos ficticia para la autenticación
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("12345678"),
        "disabled": False,
    }
}

# Configuración JWT
SECRET_KEY = "clave_segura_de_ejemplo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10  

# ... (resto de funciones y modelos)

#BD ficticia
usuarios = [
    {"id": 1, "nombre": "Martin", "edad": 20},
    {"id": 2, "nombre": "Tovar", "edad": 21},
    {"id": 3, "nombre": "Rubio", "edad": 19},
]

#Modelo de validación pydantic
class UsuarioBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example=22)
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", example="Martín")
    edad:int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121", example=87)

#Modelo de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str]= None

#Función para verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Función para autenticar al usuario
def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

#Función para crear el token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependencia OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencia para obtener el usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_db.get(token_data.username)  # Usar users_db
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

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

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario.model_dump())

    return {
        "mensaje": "Usuario agregado",
        "datos": usuario
    }

# Actualizar usuario
@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioBase, current_user= Depends(get_current_active_user)):
    data= usuario_actualizado.model_dump()

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            data["id"]= id
            usuarios[index] = data
            return {
                "mensaje": "Usuario actualizado",
                "datos": data
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# Eliminar usuario
@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, current_user= Depends(get_current_active_user)):

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

# Autenticación
@app.post("/token", response_model=Token, tags=['Autenticación'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)  # Cambiado a users_db
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Constante corregida
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}