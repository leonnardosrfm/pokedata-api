# PokéData API

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![HTTPX](https://img.shields.io/badge/HTTPX-HTTP%20Client-5A67D8)](https://www.python-httpx.org/)

API backend desenvolvida com **FastAPI** e **PostgreSQL** para ingestão, persistência e análise de dados de Pokémon a partir da **PokéAPI**.

---

## Visão geral

O objetivo deste projeto é demonstrar competências em **backend** e **dados** por meio de uma aplicação que integra uma API externa, armazena informações em banco relacional e disponibiliza consultas e análises por meio de endpoints organizados e documentados.

Este projeto destaca principalmente:

- Consumo de API externa
- Persistência em banco relacional
- Modelagem com SQLAlchemy
- Validação com Pydantic
- Filtros e paginação
- Endpoints analíticos
- Análise estratégica de times Pokémon
- Organização em camadas com rotas e services

---

## Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **HTTPX**

---

## Principais funcionalidades

### Gestão de Pokémon
- Cadastro manual de Pokémon
- Importação individual a partir da PokéAPI
- Importação em lote para popular a base
- Listagem com filtros por nome e tipo
- Consulta por ID

### Estatísticas e análise
- Ranking dos Pokémon com maior ataque
- Ranking dos Pokémon com maior velocidade
- Médias por tipo principal
- Resumo estatístico geral da base
- Análise simplificada de times
- Análise detalhada de times
- Identificação de tipos presentes e repetidos
- Cálculo de fraquezas, resistências e imunidades
- Médias de atributos do time

---

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/pokedata-api.git
cd pokedata-api
```

### 2. Crie e ative o ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo chamado .env na raiz do projeto:

```bash
DATABASE_URL=postgresql+psycopg://postgres:SUA_SENHA@localhost:5432/pokedata
```

### 5. Inicie a aplicação

```bash
uvicorn app.main:app --reload
```

### 6. Acesse o swagger localmente

```bash
http://127.0.0.1:8000/docs
```
