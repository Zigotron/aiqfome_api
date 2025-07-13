from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from app.configuracao.banco_dados import obter_db
from app.esquemas_api import favorito as esquema_favorito
from app.operacoes_bd import favorito as operacoes_favorito
from app.operacoes_bd import cliente as operacoes_cliente
from app.servicos import api_produtos as servico_produtos

from app.servicos.auth import verificar_permissao_leitura 

# rota favoritos
roteador_favoritos = APIRouter(
    prefix="/clientes/{id}/favoritos",
    tags=["favoritos"],
    responses={404: {"description": "Não encontrado"}},
    dependencies=[Depends(verificar_permissao_leitura)]   
)

ObterDB = Depends(obter_db)


from fastapi.responses import JSONResponse

# Endpoint para adicionar um novo favorito
@roteador_favoritos.post("/", status_code=status.HTTP_201_CREATED)
async def adicionar_novo_favorito(
    id: int = Path(..., description="ID do cliente para adicionar o favorito."),
    favorito_data: esquema_favorito.FavoritoAdicionar = Body(...),
    db: Session = ObterDB
):
    # vai no banco e pega cliente
    cliente_existente = operacoes_cliente.obter_cliente_por_id(db, id)
    if not cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    favorito_existente = operacoes_favorito.obter_favorito_por_cliente_e_produto(
        db, cliente_id=id, produto_id=favorito_data.id_produto
    )
    if favorito_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este produto já está na lista de favoritos deste cliente."
        )

    # chama API externa pra ver se existe o produto
    detalhes_produto_externo = await servico_produtos.obter_produto_por_id_externo(favorito_data.id_produto)

    if not detalhes_produto_externo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado na API externa. Verifique o ID."
        )
    
    favorito_criado_dict = operacoes_favorito.adicionar_favorito(
        db=db,
        cliente_id=id,
        produto_info={
            "id": detalhes_produto_externo["id"],
            "title": detalhes_produto_externo["title"],
            "image": detalhes_produto_externo["image"],
            "price": detalhes_produto_externo["price"],
        },
        review_manual=favorito_data.review
    )

    if not favorito_criado_dict:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao adicionar favorito. Tente novamente."
        )

    # tira  a prop 'review' se ela estiver vazia
    response_data = dict(favorito_criado_dict)  
    if not response_data.get("review"):
        response_data.pop("review", None)

    return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


# Endpoint para listar  favoritos 
@roteador_favoritos.get("/", response_model=List[esquema_favorito.FavoritoResposta])
async def listar_favoritos_do_cliente(
    id: int = Path(..., description="ID do cliente para listar os favoritos."),
    skip: int = 0,
    limit: int = 100,
    db: Session = ObterDB
):
    cliente_existente = operacoes_cliente.obter_cliente_por_id(db, id)
    # nao achou 
    if not cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    lista_favoritos_cliente = operacoes_favorito.obter_favoritos_por_cliente(
        db, cliente_id=id, skip=skip, limit=limit
    )

    # removo prop se ela estiver vazia
    response_data = [
        item.dict(exclude_none=True) for item in lista_favoritos_cliente
    ]

    return JSONResponse(content=response_data)


# Endpoint para obter um favorito 
@roteador_favoritos.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_favorito_do_cliente(
    id: int = Path(..., description="ID do cliente dono do favorito."),
    produto_id: int = Path(..., description="ID do produto a ser removido da lista de favoritos."),
    db: Session = ObterDB
):
    cliente_existente = operacoes_cliente.obter_cliente_por_id(db, id)
    if not cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    # deleta no bd
    favorito_deletado = operacoes_favorito.remover_favorito_por_cliente_e_produto_id(
        db, cliente_id=id, produto_id=produto_id
    )

    if favorito_deletado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorito não encontrado para este cliente e produto."
        )
    
    return
