from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modelos_bd import produto as modelo_produto

def obter_produto_por_id(db: Session, id: int):
    # Busca um produto pelo ID (PK da tabela produtos).
    return db.query(modelo_produto.Produto).filter(modelo_produto.Produto.id == id).first()

def criar_produto_se_nao_existe(db: Session, produto_info: dict):
    # Tenta criar um produto se ele não existe.
    # Retorna o produto existente ou o recém-criado.

    produto_existente = obter_produto_por_id(db, produto_info["id"])
    if produto_existente:
        return produto_existente # Já existe, retorna o existente

    # Cria nova instância do  Produto
    novo_produto_db = modelo_produto.Produto(
        id=produto_info["id"],
        titulo=produto_info["title"],
        imagem=produto_info["image"],
        preco=produto_info["price"]
    )
    db.add(novo_produto_db)
    try:
        db.commit()
        db.refresh(novo_produto_db)
        return novo_produto_db
    except IntegrityError:
        # outro processo inseriu ao mesmo tempo
        # reverte e tenta buscar o produto que causou o conflito.
        db.rollback()
        return obter_produto_por_id(db, produto_info["id"])
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar produto no DB: {e}")
        return None
