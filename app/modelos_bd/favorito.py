from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy.schema import PrimaryKeyConstraint
from app.configuracao.banco_dados import BaseDeModelos
from app.modelos_bd.produto import Produto 

class Favorito(BaseDeModelos):
    __tablename__ = "favoritos"

    # na podem ser nulos pois são pk composta
    cliente_id = Column(BigInteger, ForeignKey("clientes.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    review = Column(String(500), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('cliente_id', 'produto_id', name='pk_favoritos_composta'),
    )

    # Relaciona com Cliente
    cliente = relationship("Cliente", back_populates="favoritos")

    # Relaciona com Produto
    produto = relationship("Produto", lazy="joined") 
