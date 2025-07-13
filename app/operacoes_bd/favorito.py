from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any

from app.modelos_bd import favorito as modelo_favorito
from app.modelos_bd import cliente as modelo_cliente
from app.modelos_bd import produto as modelo_produto
from app.esquemas_api import favorito as esquema_favorito
from app.operacoes_bd import produto as operacoes_produto
from app.esquemas_api.favorito import FavoritoResposta

# pega todos os favoritos do cliente com os produtos 
def obter_favoritos_por_cliente(db: Session, cliente_id: int, skip: int = 0, limit: int = 100) -> List[FavoritoResposta]:
    favoritos_db = db.query(modelo_favorito.Favorito).options(joinedload(modelo_favorito.Favorito.produto)).filter(
        modelo_favorito.Favorito.cliente_id == cliente_id
    ).offset(skip).limit(limit).all()

    lista_de_respostas = []
    for favorito in favoritos_db:
        kwargs = {
            "id_produto": favorito.produto_id,
            "titulo": favorito.produto.titulo,
            "imagem": favorito.produto.imagem,
            "preco": float(favorito.produto.preco),
        }

        # se tiver review, adiciona
        if favorito.review and favorito.review.strip():
            kwargs["review"] = favorito.review

        lista_de_respostas.append(FavoritoResposta(**kwargs))
    
    return lista_de_respostas

# confere se esse cliente já favoritou esse produto
def obter_favorito_por_cliente_e_produto(db: Session, cliente_id: int, produto_id: int) -> Optional[modelo_favorito.Favorito]:
    return db.query(modelo_favorito.Favorito).options(joinedload(modelo_favorito.Favorito.produto)).filter(
        modelo_favorito.Favorito.cliente_id == cliente_id,
        modelo_favorito.Favorito.produto_id == produto_id
    ).first()

# adiciona o produto na lista de favoritos se tudo  ok
def adicionar_favorito(db: Session, cliente_id: int, produto_info: dict, review_manual: Optional[str] = None) -> Optional[Dict[str, Any]]:
    cliente_existente = db.query(modelo_cliente.Cliente).filter(modelo_cliente.Cliente.id == cliente_id).first()
    if not cliente_existente:
        return None  # cliente nem existe

    produto_db = operacoes_produto.criar_produto_se_nao_existe(db, produto_info)
    if not produto_db:
        return None  

    review_para_gravar = review_manual.strip() if review_manual else None

    novo_favorito_db = modelo_favorito.Favorito(
        cliente_id=cliente_id,
        produto_id=produto_info["id"],
        review=review_para_gravar
    )
    
    db.add(novo_favorito_db)
    try:
        db.commit()
        resposta_dict = {
            "id_produto": novo_favorito_db.produto_id,
            "titulo": produto_db.titulo,
            "imagem": produto_db.imagem,
            "preco": float(produto_db.preco),
        }
        if novo_favorito_db.review and novo_favorito_db.review.strip():
            resposta_dict["review"] = novo_favorito_db.review
        return resposta_dict
    except IntegrityError:
        db.rollback()
        return None  # já tava favoritado talvez

# remove um favorito se ele estiver lá
def remover_favorito_por_cliente_e_produto_id(db: Session, cliente_id: int, produto_id: int) -> Optional[modelo_favorito.Favorito]:
    favorito_a_deletar = db.query(modelo_favorito.Favorito).filter(
        modelo_favorito.Favorito.cliente_id == cliente_id,
        modelo_favorito.Favorito.produto_id == produto_id
    ).first()

    if favorito_a_deletar:
        db.delete(favorito_a_deletar)
        db.commit()
        return favorito_a_deletar  
    return None  # nada pra deletar
