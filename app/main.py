from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine, Base
from app.api.routes.pokemon import router as pokemon_router
from app.api.routes.stats import router as stats_router
from app.api.routes.teams import router as teams_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PokéData API",
    summary="API para carregar, consultar e analisar Pokémon.",
    description="""
API backend desenvolvida com FastAPI e PostgreSQL para:

- cadastrar Pokémon manualmente
- buscar Pokémon da PokéAPI
- carregar vários Pokémon em lote
- consultar lista com filtros e paginação
- visualizar detalhes de um Pokémon por ID
- consultar estatísticas
- analisar times
""",
    version="1.0.0",
    swagger_ui_parameters={"docExpansion": "none"},
)

app.include_router(pokemon_router)
app.include_router(stats_router)
app.include_router(teams_router)


@app.get(
    "/",
    summary="Página inicial",
    description="Retorna uma mensagem simples informando que a API está rodando.",
    response_description="Mensagem de status da API.",
)
def read_root():
    return {"message": "PokéData API rodando!"}


@app.get(
    "/health",
    summary="Verificar saúde da API",
    description="Testa se a API consegue se conectar ao banco de dados.",
    response_description="Status da API e da conexão com o banco.",
)
def health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}