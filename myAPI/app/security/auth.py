from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import HTTPException, Depends, status

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