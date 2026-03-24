from fastapi import HTTPException, Depends, APIRouter, status
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)

# ----------- CRUD Usuarios -----------

# Obtener usuarios
@router.get("/", status_code=status.HTTP_200_OK)
async def obtener_usuarios(db: Session = Depends(get_db)):

    consulta_usuarios=db.query(UsuarioDB).all()

    return {
        "status": status.HTTP_200_OK,
        "total": len(consulta_usuarios),
        "data": consulta_usuarios
    }


# Obtener por ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def obtener_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return usr

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# Crear usuario
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):

    nuevoUsuario = UsuarioDB(nombre=usuario.nombre, edad=usuario.edad)
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return {
        "status": status.HTTP_201_CREATED,
        "mensaje": "Usuario agregado",
        "datos": usuario
    }


# Actualizar usuario
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(
    id: int,
    usuario_actualizado: UsuarioBase,
    _: str = Depends(verificar_Peticion)
):

    if usuario_actualizado.id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del body no coincide con la URL"
        )

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario_actualizado.dict()
            return {
                "status": status.HTTP_200_OK,
                "mensaje": "Usuario actualizado",
                "datos": usuarios[index]
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_Peticion)
):

    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "status": status.HTTP_200_OK,
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "datos": usr
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no existe"
    )