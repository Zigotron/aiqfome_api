from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship
from app.configuracao.banco_dados import BaseDeModelos 

class Cliente(BaseDeModelos):
    __tablename__ = "clientes" 

    # config da pk e cria indice para acelerar busca
    id = Column(BigInteger, primary_key=True, index=True) 

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    # relacao com a tabela  favoritos.
    favoritos = relationship("Favorito", back_populates="cliente", cascade="all, delete-orphan")
