from pydantic import BaseModel


# Esquema para a resposta  um produto.
class ProdutoResposta(BaseModel):
    id: int
    titulo: str
    imagem: str
    preco: float

    class Config:
        from_attributes = True 
        
