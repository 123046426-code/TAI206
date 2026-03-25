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
async def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {
        "status": status.HTTP_200_OK,
        "data": usuario
    }


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
    db: Session = Depends(get_db),
    _: str = Depends(verificar_Peticion)
):
    usuario= db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad
    db.commit()
    db.refresh(usuario)

    return {
        "status": status.HTTP_200_OK,
        "mensaje": "Usuario actualizado",
        "datos": usuario
    }


# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    db: Session = Depends(get_db),
    usuarioAuth: str = Depends(verificar_Peticion)
):
    usuario= db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "status": status.HTTP_200_OK,
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "datos": {
            "id": id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        }
    }