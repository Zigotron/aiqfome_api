from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.rotas import clientes, favoritos, auth  

# cria o app
app = FastAPI(
    title="API de Produtos Favoritos - AIQFOME",
    description="API para gerenciar clientes e seus produtos favoritos, integrando com uma API externa de produtos.",
    version="0.1.0",
)

# incui rotas
app.include_router(auth.roteador_auth)
app.include_router(clientes.roteador_clientes)
app.include_router(favoritos.roteador_favoritos)

# rota para checar se a API está ok
@app.get("/", tags=["status"])
async def Check_status():
    return {"mensagem": "API está online!"}

# esquema OpenAPI para adicionar segurança na API
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Define esquema de segurança Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # aplica sefgurança nos endpoints
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            # nao  aplicar segurança em rotas abertas como a raiz e login
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
