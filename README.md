# API de Produtos Favoritos - AIQFOME

Este projeto é uma API feita em Python com FastAPI para gerenciar clientes e suas listas de produtos favoritos. Ela se conecta a um banco de dados PostgreSQL e usa uma API externa (Fake Store API) para buscar detalhes dos produtos.

## Como Rodar o Projeto

Para rodar este projeto, você precisará ter Python e PostgreSQL instalados em sua máquina.

1.  **Pré-requisitos:**
    * Tenha o **Python 3.11** (ou mais novo) instalado.
    * Tenha acesso a um servidor **PostgreSQL** rodando (pode ser na sua máquina ou em outro lugar, desde que seja acessível).

2.  **Baixe o Projeto:**
    * Se for um arquivo ZIP, descompacte-o.
    * Se for do Git, clone o repositório:
        ```bash
        git clone https://github.com/Zigotron/aiqfome_api.git
        cd aiqfome_api  # Acesse a pasta clonada
        ```

3.  **Configure as Informações:**
    * Na pasta principal (raiz) do projeto, você verá um arquivo chamado `.env`.
    * **Abra o arquivo `.env`** e preencha as informações do seu banco de dados.
        * **Importante:** A `URL_SERVIDOR_DADOS` deve apontar para o seu PostgreSQL.
        * Exemplo de como deve ficar seu `.env`:

            ```
            # dados do banco de dados 
            URL_SERVIDOR_DADOS = "postgresql://SEU_USUARIOs:SUA_SENHA@localhost:5432/"
            NOME_BANCO_DADOS = "db_aiqfome"

            # url da api externa de produtos 
            URL_API_PRODUTOS_EXTERNA="https://fakestoreapi.com"

            # para controlar o token
            SECRET_KEY="dGrRytffBZv0CQ6zIj67OTZB7vuGn2iJG3N6ueKMxyQ"
            ALGORITHM = "HS256"
            EXPIRA_EM_MINUTOS = 30

            ```
            Na variável `URL_SERVIDOR_DADOS`, substitua `SEU_USUARIO` e `SUA_SENHA` pelo nome de usuário e a senha que você utiliza no seu PostgreSQL.  
            Esse usuário precisa ter permissão para executar comandos DDL (como criar tabelas).

            Se o banco estiver hospedado em outro servidor, substitua `localhost` pelo IP ou hostname do servidor PostgreSQL remoto.

            As outras configurações não precisam ser editadas. 

4.  **Prepare o Ambiente Python:**

    * Abra o terminal na pasta principal do projeto.

    * Crie um ambiente virtual (para não misturar as instalações):

        ```bash
        python -m venv venv
        ```

    * Ative o ambiente virtual:

        * No Windows: `.\venv\Scripts\activate`

        * No macOS/Linux: `source venv/bin/activate`

    * Instale as bibliotecas que o projeto precisa:

        ```bash
        pip install -r requirements.txt
        ```

5.  **Crie o Banco de Dados e as Tabelas:**

    O usuário do PostgreSQL que você configurou no `.env` (geralmente `postgres`) **precisa ter permissão para criar e apagar bancos de dados**.

    Você tem duas opções para criar o banco de dados e as tabelas:

    * **Opção A: Usando o script Python (Recomendado)**
        Este script Python irá criar o banco de dados `db_aiqfome` e todas as tabelas.
        No terminal, na pasta raiz do projeto e com o ambiente virtual ativado, digite:
        ```bash
        python setup_db.py
        ```
        Ele vai mostrar mensagens de "Banco e tabelas criados com sucesso!".

    * **Opção B: Usando o script SQL diretamente (via pgAdmin)**
        1.  **Etapa 1: Criar o Banco de Dados `db_aiqfome`**
            * Abra o **pgAdmin 4** (ou outra ferramenta de acesso ao PostgreSQL).
            * Conecte-se a **qualquer banco de dados existente** que você tenha acesso (por exemplo, o banco `postgres` padrão).
            * Abra a **Query Tool** (Ferramenta de Consulta).
            * **Copie e cole o comando abaixo** na Query Tool e execute:
                ```sql
                DROP DATABASE IF EXISTS db_aiqfome;
                CREATE DATABASE db_aiqfome;
                ```
            * Após a execução, **recarregue a lista de bancos de dados no pgAdmin** (clique com o botão direito em `Databases` e selecione `Refresh`). Você verá `db_aiqfome` na lista.

        2.  **Etapa 2: Criar as Tabelas no `db_aiqfome`**
            * No pgAdmin, abra uma **NOVA Query Tool** e **conecte-a ao banco de dados `db_aiqfome`** (clique com o botão direito em `db_aiqfome` e selecione `Query Tool...`).
            * **Copie e cole todo o conteúdo** do arquivo `criar_banco.sql` (que estará na raiz do projeto) na nova Query Tool e execute.


## Estrutura do Banco de Dados

O banco de dados é modelado para evitar redundância e otimizar os relacionamentos. Temos três tabelas principais: `clientes`, `produtos` e `favoritos`.

![Diagrama das Tabelas do Banco de Dados](imgs/diagrama.png)

* **`clientes`**: Armazena as informações básicas dos usuários.
* **`produtos`**: Guarda os detalhes únicos dos produtos da API externa, evitando que dados como título, imagem e preço se repitam.
* **`favoritos`**: Funciona como uma tabela de ligação entre clientes e produtos, armazenando qual cliente favoritou qual produto, além de um campo para um review manual.

## Como Usar a API

Após iniciar a API, você pode interagir com ela através da documentação interativa (Swagger UI) disponível em `http://localhost:8000/docs`.

### Autenticação e Autorização (POC)

Para esta Prova de Conceito (POC), a API possui um sistema de autenticação simplificado por token e autorização baseada em "roles" (funções).

* **Arquivo `usuarios.json`**: Na raiz do projeto, você encontrará um arquivo `usuarios.json` com usuários mockados para testes. Cada usuário tem um `username`, `password` e `role` (`admin` ou `reader`).
    * **`admin`**: Pode usar todos os endpoints (criar, ler, atualizar, deletar).
    * **`reader`**: Pode usar apenas os endpoints `GET` (leitura).

#### Fluxo de Uso:

1.  **Checar Status da API.**
2.  **Fazer Login** para obter um token de acesso.
3.  **Autorizar no Swagger UI** com o token recebido.
4.  **Usar os Outros Endpoints** conforme a role do usuário.
5.  Você pode trocar de usuário no `usuarios.json` e refazer o login para testar diferentes roles.

### Endpoints da API (Ordem de Execução Sugerida)

#### 1. Checar Status da API

* **Nome:** Checar Status
* **Verbo HTTP:** `GET`
* **Resumo:** Verifica se a API está online e funcionando.
* **Instrução de Uso:** Não requer autenticação. Basta acessar a URL no navegador ou usar o Swagger UI.
    * URL: `http://localhost:8000/`
    
#### 2. Login de Usuário

* **Nome:** Login
* **Verbo HTTP:** `POST`
* **Resumo:** Autentica um usuário e retorna um token de acesso.
* **Instrução de Uso:**
    1.  No Swagger UI, expanda o endpoint `POST /auth/login`.
    2.  Clique em "Try it out".
    3.  No "Request body", insira as credenciais de um usuário do `usuarios.json` (ex: `{"username": "alice", "password": "123"}`).

        ![0](imgs/auth.png)

    4.  Clique em "Execute".
    5.  **Após receber o token (`access_token`) na resposta:**
        * Copie o valor do `access_token` sem as apsas.
        
            ![1](imgs/auth_tok.png)

        * Clique no botão verde "Authorize" (ou ícone de cadeado) no canto superior direito do Swagger UI.

            ![1](imgs/auth_botao.png)

        * No campo "Value", digite `Bearer <SEU_TOKEN_AQUI>` (substitua `<SEU_TOKEN_AQUI>` pelo token copiado).

            ![2](imgs/auth_pop.png)

        * Clique em "Authorize" e depois "Close". Agora você está autenticado para usar os outros métodos. 
        Se quiser trocar de usuario para testar outro usuario com menos permissoes , basta abrir esse popup novamente clicando no botão "Authorize" e clique no botão "Logout". 

            ![2](imgs/auth_pop2.png)
        
        Em seguida repita os passos de login com outro usuario, copie o token e autorize novamente outro usuario.
  

#### 3. Criar Novo Cliente

* **Nome:** Criar Novo Cliente
* **Verbo HTTP:** `POST`
* **Resumo:** Cadastra um novo cliente na plataforma.
* **Instrução de Uso:** Requer autenticação (role `admin`).
    1.  No Swagger UI, expanda o endpoint `POST /clientes`.
    2.  Clique em "Try it out".
    3.  No "Request body", insira os dados do novo cliente (nome e e-mail). O e-mail deve ser único.
    4.  Clique em "Execute".

        ![Criar Novo Cliente](imgs/criar_novo_cliente.png)

#### 4. Listar Clientes

* **Nome:** Listar Clientes
* **Verbo HTTP:** `GET`
* **Resumo:** Lista todos os clientes cadastrados, com opção de paginação.
* **Instrução de Uso:** Requer autenticação (role `admin` ou `reader`).
    1.  No Swagger UI, expanda o endpoint `GET /clientes`.
    2.  Clique em "Try it out".
    3.  (Opcional) Ajuste `skip` e `limit` para paginação.
    4.  Clique em "Execute".

        ![Listar Clientes](imgs/listar_cliente.png)

#### 5. Obter Cliente por ID

* **Nome:** Obter Cliente
* **Verbo HTTP:** `GET`
* **Resumo:** Busca os detalhes de um cliente específico pelo seu ID.
* **Instrução de Uso:** Requer autenticação (role `admin` ou `reader`).
    1.  No Swagger UI, expanda o endpoint `GET /clientes/{id}`.
    2.  Clique em "Try it out".
    3.  No campo `id` (parâmetro de caminho), digite o ID do cliente.
    4.  Clique em "Execute".

        ![Obter Cliente](imgs/obter_cliente.png)

#### 6. Atualizar Dados Cliente

* **Nome:** Atualizar Dados Cliente
* **Verbo HTTP:** `PUT`
* **Resumo:** Atualiza as informações de um cliente existente.
* **Instrução de Uso:** Requer autenticação (role `admin`).
    1.  No Swagger UI, expanda o endpoint `PUT /clientes/{id}`.
    2.  Clique em "Try it out".
    3.  No campo `id`, digite o ID do cliente a ser atualizado.
    4.  No "Request body", insira os campos que deseja atualizar (nome e/ou e-mail).

        ![5](imgs/cliente_atualiza.png)

    5.  Clique em "Execute". Os dados são atualizados.

        ![5](imgs/cliente_atualiza_2.png)

#### 7. Deletar Cliente Existente

* **Nome:** Deletar Cliente Existente
* **Verbo HTTP:** `DELETE`
* **Resumo:** Remove um cliente da plataforma.
* **Instrução de Uso:** Requer autenticação (role `admin`).
    1.  No Swagger UI, expanda o endpoint `DELETE /clientes/{id}`.
    2.  Clique em "Try it out".
    3.  No campo `id`, digite o ID do cliente a ser deletado.
    4.  Clique em "Execute".
    
#### 8. Adicionar Novo Favorito

* **Nome:** Adicionar Novo Favorito
* **Verbo HTTP:** `POST`
* **Resumo:** Adiciona um produto à lista de favoritos de um cliente. O produto é validado com a API externa.
* **Instrução de Uso:** Requer autenticação (role `admin`).
    1.  No Swagger UI, expanda o endpoint `POST /clientes/{id}/favoritos`.
    2.  Clique em "Try it out".
    3.  No campo `id`, digite o ID do cliente.
    4.  No "Request body", insira o `id_produto` da API externa e, opcionalmente, um `review` textual.
    5.  Clique em "Execute".

        ![6](imgs/favorito_com_review.png)

        Se preferir não colocar `review` na hora de favoritar, basta não enviar esse campo. Ficando apenas o `id_produto`

         ![6](imgs/favorito_com_sem_review.png)

#### 9. Listar Favoritos do Cliente

* **Nome:** Listar Favoritos do Cliente
* **Verbo HTTP:** `GET`
* **Resumo:** Lista todos os produtos favoritos de um cliente específico.
* **Instrução de Uso:** Requer autenticação (role `admin` ou `reader`).
    1.  No Swagger UI, expanda o endpoint `GET /clientes/{id}/favoritos`.
    2.  Clique em "Try it out".
    3.  No campo `id`, digite o ID do cliente.
    4.  (Opcional) Ajuste `skip` e `limit` para paginação.
    5.  Clique em "Execute".

        ![Listar Favoritos do Cliente](imgs/lista_favoritos.png)

        Caso o produto favorito não tenha `review` o campo não é retornado na resposta. 

#### 10. Remover Favorito do Cliente

* **Nome:** Remover Favorito do Cliente
* **Verbo HTTP:** `DELETE`
* **Resumo:** Remove um produto específico da lista de favoritos de um cliente.
* **Instrução de Uso:** Requer autenticação (role `admin`).
    1.  No Swagger UI, expanda o endpoint `DELETE /clientes/{id}/favoritos/{produto_id}`.
    2.  Clique em "Try it out".
    3.  No campo `id`, digite o ID do cliente.
    4.  No campo `produto_id`, digite o ID do produto externo a ser removido.
    5.  Clique em "Execute".
   


