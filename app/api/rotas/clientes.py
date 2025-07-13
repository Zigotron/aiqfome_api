from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from typing import List

from app.configuracao.banco_dados import obter_db
from app.esquemas_api import cliente as esquema_cliente
from app.operacoes_bd import cliente as operacoes_cliente

from app.servicos.auth import verificar_permissao_leitura 

# Cria rota clientes
roteador_clientes = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"description": "Não encontrado"}},
    dependencies=[Depends(verificar_permissao_leitura)]  
)

#  obtem a sessão do banco de dados.
ObterDB = Depends(obter_db)

# Endpoint para criar um novo cliente.
@roteador_clientes.post("/", response_model=esquema_cliente.ClienteResposta, status_code=status.HTTP_201_CREATED)
def criar_novo_cliente(cliente: esquema_cliente.ClienteCriar, db: Session = ObterDB):
    
    cliente_existente = operacoes_cliente.obter_cliente_por_email(db, email=cliente.email)
    if cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um cliente com este e-mail."
        )
    
    cliente_criado = operacoes_cliente.criar_cliente(db=db, cliente=cliente)
    if not cliente_criado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar cliente. Tente novamente."
        )
    return cliente_criado

# Endpoint para listar todos os clientes.
@roteador_clientes.get("/", response_model=List[esquema_cliente.ClienteResposta])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = ObterDB):
    
    clientes = operacoes_cliente.obter_clientes(db, skip=skip, limit=limit)
    return clientes

# Endpoint para buscar um cliente pelo id
@roteador_clientes.get("/{id}", response_model=esquema_cliente.ClienteResposta)
def obter_cliente(id: int = Path(..., description="ID do cliente a ser buscado."), db: Session = ObterDB):
    
    cliente = operacoes_cliente.obter_cliente_por_id(db, id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )
    return cliente


# Endpoint para atualizar os dados de cliente 
@roteador_clientes.put("/{id}", response_model=esquema_cliente.ClienteResposta)
def atualizar_dados_cliente(
    id: int = Path(..., description="ID do cliente a ser atualizado."),
    cliente_atualizar: esquema_cliente.ClienteAtualizar = Body(...), 
    db: Session = ObterDB
):
  
    cliente_existente = operacoes_cliente.obter_cliente_por_id(db, id)
    if cliente_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )
    
    if cliente_atualizar.email is not None and cliente_atualizar.email != cliente_existente.email:
        cliente_com_novo_email = operacoes_cliente.obter_cliente_por_email(db, email=cliente_atualizar.email)
        if cliente_com_novo_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro cliente com este e-mail."
            )

    cliente_atualizado = operacoes_cliente.atualizar_cliente(db=db, id=id, cliente_atualizar=cliente_atualizar)
    if not cliente_atualizado:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar cliente. Tente novamente."
        )
    return cliente_atualizado


# Endpoint para deletar  cliente
@roteador_clientes.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente_existente(id: int = Path(..., description="ID do cliente a ser deletado."), db: Session = ObterDB):
    
    cliente_deletado = operacoes_cliente.deletar_cliente(db, id)
    if cliente_deletado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )
    return
