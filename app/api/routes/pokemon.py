from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pokemon
from app.pokeapi import fetch_pokemon_from_pokeapi
from app.schemas import PokemonCreate, PokemonListResponse, PokemonResponse
from app.services.pokemon_service import create_pokemon_from_api_data

router = APIRouter(prefix="/pokemon", tags=["Pokémon"])


@router.post(
    "",
    response_model=PokemonResponse,
    summary="Cadastrar Pokémon manualmente",
    description="Cadastra um Pokémon manualmente no banco de dados.",
    response_description="Pokémon cadastrado com sucesso.",
)
def create_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    existing = db.query(Pokemon).filter(Pokemon.name == pokemon.name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Pokémon já cadastrado.")

    new_pokemon = Pokemon(
        pokeapi_id=pokemon.pokeapi_id,
        name=pokemon.name.lower(),
        type_1=pokemon.type_1.lower(),
        type_2=pokemon.type_2.lower() if pokemon.type_2 else None,
        height=pokemon.height,
        weight=pokemon.weight,
        base_experience=pokemon.base_experience,
        hp=pokemon.hp,
        attack=pokemon.attack,
        defense=pokemon.defense,
        special_attack=pokemon.special_attack,
        special_defense=pokemon.special_defense,
        speed=pokemon.speed,
    )
    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    return new_pokemon


@router.get(
    "",
    response_model=PokemonListResponse,
    summary="Listar Pokémon",
    description="Lista os Pokémon cadastrados, com filtro por nome, tipo e paginação.",
    response_description="Lista paginada de Pokémon encontrados.",
)
def list_pokemon(
    name: str | None = Query(default=None, description="Filtra Pokémon pelo nome."),
    type: str | None = Query(default=None, description="Filtra Pokémon por tipo."),
    limit: int = Query(default=20, ge=1, le=100, description="Quantidade máxima de registros."),
    offset: int = Query(default=0, ge=0, description="Quantidade de registros a pular."),
    db: Session = Depends(get_db),
):
    query = db.query(Pokemon)

    if name:
        query = query.filter(Pokemon.name.ilike(f"%{name}%"))

    if type:
        query = query.filter(
            (Pokemon.type_1.ilike(type)) |
            (Pokemon.type_2.ilike(type))
        )

    total = query.count()
    items = query.order_by(Pokemon.id).limit(limit).offset(offset).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


@router.get(
    "/{pokemon_id}",
    response_model=PokemonResponse,
    summary="Buscar Pokémon por ID",
    description="Retorna os detalhes de um Pokémon salvo no banco a partir do ID interno.",
    response_description="Dados do Pokémon encontrado.",
)
def get_pokemon_by_id(
    pokemon_id: int = Path(..., ge=1, description="ID interno do Pokémon no banco."),
    db: Session = Depends(get_db),
):
    pokemon = db.get(Pokemon, pokemon_id)

    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado.")

    return pokemon


@router.post(
    "/load/{name}",
    response_model=PokemonResponse,
    summary="Carregar um Pokémon da PokéAPI",
    description="Busca um Pokémon na PokéAPI pelo nome e salva no banco de dados.",
    response_description="Pokémon carregado com sucesso.",
)
def load_pokemon_from_api(
    name: str = Path(..., description="Nome do Pokémon que será buscado na PokéAPI."),
    db: Session = Depends(get_db),
):
    existing = db.query(Pokemon).filter(Pokemon.name == name.lower()).first()
    if existing:
        return existing

    data = fetch_pokemon_from_pokeapi(name)
    if not data:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado na PokéAPI.")

    try:
        new_pokemon = create_pokemon_from_api_data(data)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    db.add(new_pokemon)
    db.commit()
    db.refresh(new_pokemon)
    return new_pokemon


@router.post(
    "/load-batch",
    response_model=list[PokemonResponse],
    summary="Carregar vários Pokémon da PokéAPI",
    description="Busca vários Pokémon da PokéAPI por ID e salva no banco de dados.",
    response_description="Lista de Pokémon carregados.",
)
def load_pokemon_batch(
    limit: int = Query(default=20, ge=1, le=151, description="Quantidade de Pokémon a carregar."),
    db: Session = Depends(get_db),
):
    loaded_pokemon = []

    for pokemon_id in range(1, limit + 1):
        data = fetch_pokemon_from_pokeapi(pokemon_id)
        if not data:
            continue

        existing = db.query(Pokemon).filter(Pokemon.name == data["name"]).first()
        if existing:
            loaded_pokemon.append(existing)
            continue

        try:
            new_pokemon = create_pokemon_from_api_data(data)
        except ValueError:
            continue

        db.add(new_pokemon)
        db.commit()
        db.refresh(new_pokemon)
        loaded_pokemon.append(new_pokemon)

    return loaded_pokemon