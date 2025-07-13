
from pydantic import BaseModel, Field
from typing import Optional

#b para adicionar um novo favorito
class FavoritoAdicionar(BaseModel):
    id_produto: int
    review: Optional[str] = None

# para dados de resposta
class FavoritoResposta(BaseModel):
    id_produto: int
    titulo: str
    imagem: str
    preco: float
    review: Optional[str] = None

    # config de mapeamento para remover props nulas
    class Config:
        orm_mode = True
        exclude_none = True
