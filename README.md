# PokéData API

API backend desenvolvida com **FastAPI** e **PostgreSQL** para ingestão, consulta e análise de dados de Pokémon a partir da **PokéAPI**.

## Objetivo

Este projeto foi criado com foco em **backend** e **dados**, demonstrando:

- consumo de API externa
- persistência em banco relacional
- modelagem com SQLAlchemy
- filtros e paginação
- endpoints analíticos
- análise de times Pokémon
- organização em camadas com rotas e services

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- HTTPX

## Funcionalidades

### Pokémon
- cadastrar Pokémon manualmente
- carregar um Pokémon da PokéAPI
- carregar vários Pokémon em lote
- listar Pokémon com filtro por nome e tipo
- paginação
- buscar Pokémon por ID

### Estatísticas
- top Pokémon por ataque
- top Pokémon por velocidade
- médias por tipo principal
- resumo geral da base

### Times
- análises de time
- tipos presentes
- tipos repetidos
- fraquezas
- resistências
- imunidades
- médias de stats do time

## Como rodar o projeto:
Criar e ativar ambiente virtual

No Windows:

python -m venv .venv
.venv\Scripts\activate

2. Instalar dependências
pip install -r requirements.txt

3. Configurar .env
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/pokedata

4. Rodar a API
uvicorn app.main:app --reload

5. Abrir a documentação
http://127.0.0.1:8000/docs