from sqlalchemy import Column, String, Integer, DECIMAL
from app.configuracao.banco_dados import BaseDeModelos

class Produto(BaseDeModelos):
    __tablename__ = "produtos" 

    # ID do produto da API externa 
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    imagem = Column(String, nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)
