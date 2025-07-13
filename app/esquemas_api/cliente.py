from pydantic import BaseModel, EmailStr
from typing import Optional

# esquema do ciente
class ClienteBase(BaseModel):
  
    nome: str
    email: EmailStr

class ClienteCriar(ClienteBase):
    pass

# equema para atualizar u cliente 
class ClienteAtualizar(ClienteBase):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

# resposta da API 
class ClienteResposta(ClienteBase):
    id: int 

    # config de mapeamento pydantic X SQLAlchemy
    class Config:
        from_attributes = True 
