from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modelos_bd import cliente as modelo_cliente
from app.esquemas_api import cliente as esquema_cliente

# pega cliente por id
def obter_cliente_por_id(db: Session, id: int):
    return db.query(modelo_cliente.Cliente).filter(modelo_cliente.Cliente.id == id).first()

# busca por email..
def obter_cliente_por_email(db: Session, email: str):
    return db.query(modelo_cliente.Cliente).filter(modelo_cliente.Cliente.email == email).first()

# lista geral   com limite
def obter_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(modelo_cliente.Cliente).offset(skip).limit(limit).all()

# cria o  cliente no banco
def criar_cliente(db: Session, cliente: esquema_cliente.ClienteCriar):
    novo_cliente_db = modelo_cliente.Cliente(
        nome=cliente.nome,
        email=cliente.email
    )
    db.add(novo_cliente_db)
    try:
        db.commit()
        db.refresh(novo_cliente_db)
        return novo_cliente_db
    except IntegrityError:
        db.rollback()
        return None

# atualiza cliente se ele existir
def atualizar_cliente(db: Session, id: int, cliente_atualizar: esquema_cliente.ClienteAtualizar):
    cliente_db = obter_cliente_por_id(db, id)
    if cliente_db:
        for key, value in cliente_atualizar.model_dump(exclude_unset=True).items():
            setattr(cliente_db, key, value)

        try:
            db.commit()
            db.refresh(cliente_db)
            return cliente_db
        except IntegrityError:
            db.rollback()
            return None
    return None

# deleta cliente... se der
def deletar_cliente(db: Session, id: int):
    cliente_db = obter_cliente_por_id(db, id)
    if cliente_db:
        db.delete(cliente_db)
        db.commit()
        return cliente_db
    return None
