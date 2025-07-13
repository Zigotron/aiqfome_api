from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import urljoin

class Configuracoes(BaseSettings):

    # Variáveis do .env para o banco de dados
    URL_SERVIDOR_DADOS: str
    NOME_BANCO_DADOS: str

    # Variável para a API externa de produtos
    URL_API_PRODUTOS_EXTERNA: str

    # Configuração para carregar variáveis do .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def URL_BANCO_DADOS_COMPLETA(self) -> str:
        # Monta a URL
        base_url_ajustada = self.URL_SERVIDOR_DADOS
        if not base_url_ajustada.endswith('/'):
            base_url_ajustada += '/'
        return f"{base_url_ajustada}{self.NOME_BANCO_DADOS}"

# Cria  configurações
configuracoes = Configuracoes()
