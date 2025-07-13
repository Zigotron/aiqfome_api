# setup_db.py

import psycopg2
from dotenv import load_dotenv
import os
from urllib.parse import urlparse, urljoin

load_dotenv()

base_url = os.getenv("URL_SERVIDOR_DADOS")
nome_banco = os.getenv("NOME_BANCO_DADOS")

if not base_url or not nome_banco:
    raise ValueError("As variáveis URL_SERVIDOR_DADOS e NOME_BANCO_DADOS precisam estar definidas no .env")

db_url = urljoin(base_url, nome_banco)

parsed = urlparse(base_url)
user = parsed.username
password = parsed.password
host = parsed.hostname
port = parsed.port

print(f"Iniciando configuração do banco de dados '{nome_banco}' em {host}:{port}...")

# Etapa 1: Criar/Recriar o banco de dados
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    print(f"  Verificando e recriando o banco de dados '{nome_banco}'...")
    cur.execute(f"DROP DATABASE IF EXISTS {nome_banco};")
    cur.execute(f"CREATE DATABASE {nome_banco};")
    
    cur.close()
    conn.close()
    print(f"  Banco de dados '{nome_banco}' criado/recriado com sucesso.")

except psycopg2.Error as e:
    print(f"Erro na Etapa 1 ao criar o banco de dados: {e}")
    print("Verifique se o PostgreSQL está rodando e se as credenciais no .env têm permissões de superusuário.")
    exit(1)


# Etapa 2: Criar as tabelas dentro do banco de dados recém-criado
try:
    print(f"Conectando ao banco '{nome_banco}' para criar as tabelas...")
    conn2 = psycopg2.connect(
        dbname=nome_banco,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn2.autocommit = False
    cur2 = conn2.cursor()

    # Script SQL para criar as tabelas com as novas definições
    sql_tabelas = """
    -- Tabela de Clientes: Permanece a mesma
    CREATE TABLE IF NOT EXISTS clientes (
        id BIGSERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes (email);

    -- NOVA Tabela de Produtos: Armazena detalhes únicos dos produtos externos
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY, -- ID do produto da API externa
        titulo VARCHAR(255) NOT NULL,
        imagem VARCHAR(255) NOT NULL,
        preco DECIMAL(10, 2) NOT NULL
    );
    -- Índice para buscas rápidas por ID de produto
    CREATE INDEX IF NOT EXISTS idx_produtos_id ON produtos (id);


    -- Tabela de Favoritos: Modificada para ser uma tabela de junção
    CREATE TABLE IF NOT EXISTS favoritos (
        cliente_id BIGINT NOT NULL,          -- Chave Estrangeira para clientes.id
        produto_id INTEGER NOT NULL,         -- Chave Estrangeira para produtos.id
        review VARCHAR(500),                 -- Campo para review textual (pode ser NULL)
        
        -- Chave Primária Composta: Garante unicidade de (cliente, produto)
        PRIMARY KEY (cliente_id, produto_id), 

        -- Restrição de Chave Estrangeira para a tabela 'clientes'
        CONSTRAINT fk_favoritos_cliente
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE,
        
        -- Restrição de Chave Estrangeira para a NOVA tabela 'produtos'
        CONSTRAINT fk_favoritos_produto
            FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
    );

    -- Índices para otimizar buscas na tabela de favoritos
    CREATE INDEX IF NOT EXISTS idx_favoritos_cliente_id ON favoritos (cliente_id);
    CREATE INDEX IF NOT EXISTS idx_favoritos_produto_id ON favoritos (produto_id);
    """
    
    print("  Executando script de criação das tabelas...")
    cur2.execute(sql_tabelas)
    conn2.commit()
    
    cur2.execute("SELECT 'Banco e tabelas criados com sucesso!' AS status;")
    print(cur2.fetchone()[0])

    cur2.close()
    conn2.close()

except psycopg2.Error as e:
    print(f"Erro na Etapa 2 ao criar as tabelas: {e}")
    print("Verifique a sintaxe SQL do script de tabelas e se as permissões estão corretas.")
    exit(1)

print("\nConfiguração do banco de dados concluída com sucesso!")
print("Agora pode iniciar a API.")
