from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
import json

load_dotenv()  # carrega .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRA_EM_MINUTOS = int(os.getenv("EXPIRA_EM_MINUTOS", 30))

security = HTTPBearer()  # auth por bearer

# caminho json de usuarios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_USUARIOS = os.path.join(BASE_DIR, "usuarios.json")

# carrega usuarios do json
with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as f:
    usuarios_lista = json.load(f)
    USUARIOS = {u["username"]: u for u in usuarios_lista}  

# cria o jwt com sub e role
def criar_token_jwt(sub: str, role: str) -> str:
    expira = datetime.utcnow() + timedelta(minutes=EXPIRA_EM_MINUTOS)
    payload = {"sub": sub, "role": role, "exp": expira}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# valida login no json
def autenticar_usuario(username: str, senha: str):
    usuario = USUARIOS.get(username)
    if usuario and usuario["senha"] == senha:
        return usuario
    return None

# checa se o token é válido e extrai dados
def validar_token_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        role = payload.get("role")
        if usuario_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token JWT inválido falta usuario ou role.",
            )
        return {"id": usuario_id, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

# retorna usuário autenticado 
def get_usuario_autenticado(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    token = credentials.credentials
    usuario = validar_token_jwt(token)
    return usuario

# checa se o user pode acessar o método
def verificar_permissao_leitura(
    usuario: dict = Depends(get_usuario_autenticado),
    request: Request = None
):
    if usuario["role"] == "admin":
        return usuario  # admin pode td

    if usuario["role"] == "reader" and request.method == "GET":
        return usuario  # reader só get

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permissão negada para este recurso",
    )
