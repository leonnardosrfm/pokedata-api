from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pokemon
from app.schemas import PokemonResponse, StatsSummaryResponse, TypeStatsResponse

router = APIRouter(prefix="/stats", tags=["Estatísticas"])


@router.get(
    "/top-attack",
    response_model=list[PokemonResponse],
    summary="Top Pokémon por ataque",
    description="Retorna os Pokémon com maior valor de ataque.",
    response_description="Lista dos Pokémon com maior ataque.",
)
def get_top_attack_pokemon(
    limit: int = Query(default=10, ge=1, le=50, description="Quantidade máxima de Pokémon a retornar."),
    db: Session = Depends(get_db),
):
    return (
        db.query(Pokemon)
        .order_by(Pokemon.attack.desc(), Pokemon.id.asc())
        .limit(limit)
        .all()
    )


@router.get(
    "/top-speed",
    response_model=list[PokemonResponse],
    summary="Top Pokémon por velocidade",
    description="Retorna os Pokémon com maior valor de velocidade.",
    response_description="Lista dos Pokémon com maior velocidade.",
)
def get_top_speed_pokemon(
    limit: int = Query(default=10, ge=1, le=50, description="Quantidade máxima de Pokémon a retornar."),
    db: Session = Depends(get_db),
):
    return (
        db.query(Pokemon)
        .order_by(Pokemon.speed.desc(), Pokemon.id.asc())
        .limit(limit)
        .all()
    )


@router.get(
    "/by-type",
    response_model=list[TypeStatsResponse],
    summary="Médias por tipo principal",
    description="Retorna métricas agregadas por tipo principal dos Pokémon cadastrados.",
    response_description="Lista de métricas por tipo principal.",
)
def get_stats_by_type(db: Session = Depends(get_db)):
    results = (
        db.query(
            Pokemon.type_1.label("type"),
            func.count(Pokemon.id).label("total_pokemon"),
            func.avg(Pokemon.hp).label("average_hp"),
            func.avg(Pokemon.attack).label("average_attack"),
            func.avg(Pokemon.special_attack).label("average_special_attack"),
            func.avg(Pokemon.defense).label("average_defense"),
            func.avg(Pokemon.special_defense).label("average_special_defense"),
            func.avg(Pokemon.speed).label("average_speed"),
        )
        .group_by(Pokemon.type_1)
        .order_by(func.avg(Pokemon.attack).desc())
        .all()
    )

    return [
        {
            "type": row.type,
            "total_pokemon": row.total_pokemon,
            "average_hp": round(float(row.average_hp), 2),
            "average_attack": round(float(row.average_attack), 2),
            "average_special_attack": round(float(row.average_special_attack), 2),
            "average_defense": round(float(row.average_defense), 2),
            "average_special_defense": round(float(row.average_special_defense), 2),
            "average_speed": round(float(row.average_speed), 2),
        }
        for row in results
    ]


@router.get(
    "/summary",
    response_model=StatsSummaryResponse,
    summary="Resumo geral dos stats",
    description="Retorna métricas gerais da base de Pokémon cadastrada.",
    response_description="Resumo geral dos dados.",
)
def get_stats_summary(db: Session = Depends(get_db)):
    result = db.query(
        func.count(Pokemon.id).label("total_pokemon"),
        func.avg(Pokemon.hp).label("average_hp"),
        func.avg(Pokemon.attack).label("average_attack"),
        func.avg(Pokemon.special_attack).label("average_special_attack"),
        func.avg(Pokemon.defense).label("average_defense"),
        func.avg(Pokemon.special_defense).label("average_special_defense"),
        func.avg(Pokemon.speed).label("average_speed"),
        func.avg(Pokemon.height).label("average_height"),
        func.avg(Pokemon.weight).label("average_weight"),
    ).one()

    return {
        "total_pokemon": result.total_pokemon,
        "average_hp": round(float(result.average_hp or 0), 2),
        "average_attack": round(float(result.average_attack or 0), 2),
        "average_special_attack": round(float(result.average_special_attack or 0), 2),
        "average_defense": round(float(result.average_defense or 0), 2),
        "average_special_defense": round(float(result.average_special_defense or 0), 2),
        "average_speed": round(float(result.average_speed or 0), 2),
        "average_height": round(float(result.average_height or 0), 2),
        "average_weight": round(float(result.average_weight or 0), 2),
    }