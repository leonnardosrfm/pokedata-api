from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Pokemon
from app.type_chart import ATTACK_TYPES, get_type_multiplier


def build_team_type_analysis(pokemon_list: list[Pokemon]):
    weaknesses = []
    resistances = []
    immunities = []

    for attack_type in ATTACK_TYPES:
        weak_names = []
        weak_multipliers = []

        resist_names = []
        resist_multipliers = []

        immune_names = []

        for pokemon in pokemon_list:
            defending_types = [pokemon.type_1]
            if pokemon.type_2:
                defending_types.append(pokemon.type_2)

            multiplier = get_type_multiplier(attack_type, defending_types)

            if multiplier == 0:
                immune_names.append(pokemon.name)
            elif multiplier > 1:
                weak_names.append(pokemon.name)
                weak_multipliers.append(multiplier)
            elif multiplier < 1:
                resist_names.append(pokemon.name)
                resist_multipliers.append(multiplier)

        if weak_names:
            weaknesses.append(
                {
                    "type": attack_type,
                    "count": len(weak_names),
                    "pokemon": sorted(weak_names),
                    "average_multiplier": round(sum(weak_multipliers) / len(weak_multipliers), 2),
                }
            )

        if resist_names:
            resistances.append(
                {
                    "type": attack_type,
                    "count": len(resist_names),
                    "pokemon": sorted(resist_names),
                    "average_multiplier": round(sum(resist_multipliers) / len(resist_multipliers), 2),
                }
            )

        if immune_names:
            immunities.append(
                {
                    "type": attack_type,
                    "count": len(immune_names),
                    "pokemon": sorted(immune_names),
                    "average_multiplier": 0.0,
                }
            )

    weaknesses.sort(key=lambda item: (-item["count"], -item["average_multiplier"], item["type"]))
    resistances.sort(key=lambda item: (-item["count"], item["average_multiplier"], item["type"]))
    immunities.sort(key=lambda item: (-item["count"], item["type"]))

    return weaknesses, resistances, immunities


def get_team_base_data(team_names: list[str], db: Session):
    normalized_names = [name.lower().strip() for name in team_names]

    if len(normalized_names) < 1 or len(normalized_names) > 6:
        raise HTTPException(status_code=400, detail="O time deve ter entre 1 e 6 Pokémon.")

    pokemon_list = db.query(Pokemon).filter(Pokemon.name.in_(normalized_names)).all()

    found_names = {pokemon.name for pokemon in pokemon_list}
    missing_pokemon = [name for name in normalized_names if name not in found_names]

    if not pokemon_list:
        raise HTTPException(
            status_code=404,
            detail="Nenhum Pokémon do time foi encontrado no banco.",
        )

    types = []
    for pokemon in pokemon_list:
        types.append(pokemon.type_1)
        if pokemon.type_2:
            types.append(pokemon.type_2)

    type_count = {}
    for pokemon_type in types:
        type_count[pokemon_type] = type_count.get(pokemon_type, 0) + 1

    duplicate_types = sorted([pokemon_type for pokemon_type, count in type_count.items() if count > 1])
    types_present = sorted(type_count.keys())

    team_size = len(pokemon_list)

    total_hp = sum(pokemon.hp for pokemon in pokemon_list)
    total_attack = sum(pokemon.attack for pokemon in pokemon_list)
    total_special_attack = sum(pokemon.special_attack for pokemon in pokemon_list)
    total_defense = sum(pokemon.defense for pokemon in pokemon_list)
    total_special_defense = sum(pokemon.special_defense for pokemon in pokemon_list)
    total_speed = sum(pokemon.speed for pokemon in pokemon_list)

    weaknesses, resistances, immunities = build_team_type_analysis(pokemon_list)

    return {
        "pokemon_list": pokemon_list,
        "missing_pokemon": missing_pokemon,
        "types_present": types_present,
        "duplicate_types": duplicate_types,
        "team_size": team_size,
        "total_hp": total_hp,
        "total_attack": total_attack,
        "total_special_attack": total_special_attack,
        "total_defense": total_defense,
        "total_special_defense": total_special_defense,
        "total_speed": total_speed,
        "weaknesses": weaknesses,
        "resistances": resistances,
        "immunities": immunities,
    }


def build_simple_team_response(data: dict) -> dict:
    principais_fraquezas = [
        {"tipo": item["type"], "quantidade": item["count"]}
        for item in data["weaknesses"][:3]
    ]

    principais_resistencias = [
        {"tipo": item["type"], "quantidade": item["count"]}
        for item in data["resistances"][:3]
    ]

    imunidades = [
        {"tipo": item["type"], "quantidade": item["count"]}
        for item in data["immunities"]
    ]

    return {
        "team_size": data["team_size"],
        "tipos_presentes": data["types_present"],
        "tipos_repetidos": data["duplicate_types"],
        "principais_fraquezas": principais_fraquezas,
        "principais_resistencias": principais_resistencias,
        "imunidades": imunidades,
        "media_stats": {
            "hp": round(data["total_hp"] / data["team_size"], 2),
            "attack": round(data["total_attack"] / data["team_size"], 2),
            "special_attack": round(data["total_special_attack"] / data["team_size"], 2),
            "defense": round(data["total_defense"] / data["team_size"], 2),
            "special_defense": round(data["total_special_defense"] / data["team_size"], 2),
            "speed": round(data["total_speed"] / data["team_size"], 2),
        },
    }


def build_detailed_team_response(data: dict) -> dict:
    return {
        "team_size": data["team_size"],
        "pokemon_found": data["pokemon_list"],
        "missing_pokemon": data["missing_pokemon"],
        "types_present": data["types_present"],
        "duplicate_types": data["duplicate_types"],
        "weaknesses": data["weaknesses"],
        "resistances": data["resistances"],
        "immunities": data["immunities"],
        "average_hp": round(data["total_hp"] / data["team_size"], 2),
        "average_attack": round(data["total_attack"] / data["team_size"], 2),
        "average_special_attack": round(data["total_special_attack"] / data["team_size"], 2),
        "average_defense": round(data["total_defense"] / data["team_size"], 2),
        "average_special_defense": round(data["total_special_defense"] / data["team_size"], 2),
        "average_speed": round(data["total_speed"] / data["team_size"], 2),
        "total_attack": data["total_attack"],
        "total_defense": data["total_defense"],
        "total_speed": data["total_speed"],
    }