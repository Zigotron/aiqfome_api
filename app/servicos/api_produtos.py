
import httpx
from typing import Optional, Dict, Any
from app.configuracao.geral import configuracoes  # config api externa

URL_BASE_API_PRODUTOS = configuracoes.URL_API_PRODUTOS_EXTERNA

cliente_http = httpx.AsyncClient()  # cliente async  p/ chamadas externas

async def obter_produto_por_id_externo(produto_id: int) -> Optional[Dict[str, Any]]:
    # busca produto da api  externa

    url_completa = f"{URL_BASE_API_PRODUTOS}/products/{produto_id}"
    try:
        resposta = await cliente_http.get(url_completa)  # faz o GET
        resposta.raise_for_status()  # lança erro se status ruim

        return resposta.json()  # devolve o json
    except httpx.HTTPStatusError as e:
        print(f"Erro HTTP ao buscar produto {produto_id}: {e.response.status_code} - {e.response.text}")
        return None
    except httpx.RequestError as e:
        print(f"Erro de requisição ao buscar produto {produto_id}: {e}")  # rede ou url zuada
        return None
    except Exception as e:
        print(f"Erro inesperado ao buscar produto {produto_id}: {e}")  # deu erro geral
        return None
