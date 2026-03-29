import httpx

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"

def fetch_pokemon_from_pokeapi(name_or_id: str | int) -> dict | None:
    url = f"{POKEAPI_BASE_URL}/pokemon/{name_or_id}"
    response = httpx.get(url, timeout=10.0)

    if response.status_code != 200:
        return None

    return response.json()