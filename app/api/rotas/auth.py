from fastapi import APIRouter, HTTPException, status, Body
from app.servicos.auth import autenticar_usuario, criar_token_jwt

roteador_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# para usuario fazer login
@roteador_auth.post("/login")
def login(
    username: str = Body(..., embed=True),
    password: str = Body(..., embed=True)
):
    usuario = autenticar_usuario(username, password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )
    
    # passa o role junto
    token = criar_token_jwt(sub=usuario["id"], role=usuario["role"])
    return {"access_token": token, "token_type": "bearer"}
