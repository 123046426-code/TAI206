from fastapi import HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix= "/v1/usuarios",
    tags=["CRUD Usuarios"]
)

# ----------- CRUD Usuarios -----------

# Obtener usuarios
@router.get("/")
async def obtener_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# Obtener por ID
@router.get("/{id}")
async def obtener_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return usr

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# Crear usuario
@router.post("/")
async def agregar_usuario(usuario: UsuarioBase):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado",
        "datos": usuario
    }

# Actualizar usuario
@router.put("/{id}")
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
@router.delete("/{id}")
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