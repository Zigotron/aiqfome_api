from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.configuracao.geral import configuracoes

# Pega a URL do banco 
URL_CONEXAO_BD = configuracoes.URL_BANCO_DADOS_COMPLETA

# Cria o engine do bd
motor_sql = create_engine(URL_CONEXAO_BD, pool_pre_ping=True)

# factory de sessões para o banco de dados.
FabricaSessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor_sql)

# Base para os modelos de banco
BaseDeModelos = declarative_base()

# para injetar a sessão do banco
def obter_db():
    sessao_db: Session = FabricaSessaoLocal()
    try:
        yield sessao_db
    finally:
        sessao_db.close()
