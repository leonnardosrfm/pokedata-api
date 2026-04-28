from app.models import Pokemon


def get_pokemon_species_names_from_generation(data: dict) -> list[str]:
    species = data.get("pokemon_species", [])

    def get_species_id(item: dict) -> int:
        url = item.get("url", "").rstrip("/")
        try:
            return int(url.rsplit("/", 1)[-1])
        except ValueError:
            return 0

    ordered_species = sorted(species, key=get_species_id)
    return [item["name"] for item in ordered_species if item.get("name")]


def extract_types(data: dict) -> tuple[str, str | None]:
    type_1 = None
    type_2 = None

    for item in data["types"]:
        if item["slot"] == 1:
            type_1 = item["type"]["name"]
        elif item["slot"] == 2:
            type_2 = item["type"]["name"]

    if not type_1:
        raise ValueError("Não foi possível identificar o tipo principal.")

    return type_1, type_2


def extract_stats(data: dict) -> dict:
    stats_map = {
        "hp": 0,
        "attack": 0,
        "defense": 0,
        "special-attack": 0,
        "special-defense": 0,
        "speed": 0,
    }

    for item in data["stats"]:
        stat_name = item["stat"]["name"]
        stats_map[stat_name] = item["base_stat"]

    return {
        "hp": stats_map["hp"],
        "attack": stats_map["attack"],
        "defense": stats_map["defense"],
        "special_attack": stats_map["special-attack"],
        "special_defense": stats_map["special-defense"],
        "speed": stats_map["speed"],
    }


def create_pokemon_from_api_data(data: dict) -> Pokemon:
    type_1, type_2 = extract_types(data)
    stats = extract_stats(data)

    return Pokemon(
        pokeapi_id=data["id"],
        name=data["name"],
        type_1=type_1,
        type_2=type_2,
        height=data["height"],
        weight=data["weight"],
        base_experience=data["base_experience"],
        hp=stats["hp"],
        attack=stats["attack"],
        defense=stats["defense"],
        special_attack=stats["special_attack"],
        special_defense=stats["special_defense"],
        speed=stats["speed"],
    )
