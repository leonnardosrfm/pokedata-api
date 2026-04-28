from pydantic import BaseModel, Field, ConfigDict


class PokemonCreate(BaseModel):
    name: str = Field(
        ...,
        title="Nome",
        description="Nome do Pokémon em minúsculas.",
        examples=["pikachu"]
    )
    type_1: str = Field(
        ...,
        title="Tipo principal",
        description="Tipo principal do Pokémon.",
        examples=["electric"]
    )
    type_2: str | None = Field(
        default=None,
        title="Tipo secundário",
        description="Tipo secundário do Pokémon, se existir.",
        examples=["flying"]
    )
    pokeapi_id: int = Field(
        ...,
        title="ID da PokéAPI",
        description="Identificador original do Pokémon na PokéAPI.",
        examples=[25]
    )
    height: int = Field(
        ...,
        title="Altura",
        description="Altura do Pokémon conforme a PokéAPI.",
        examples=[4]
    )
    weight: int = Field(
        ...,
        title="Peso",
        description="Peso do Pokémon conforme a PokéAPI.",
        examples=[60]
    )
    base_experience: int | None = Field(
        default=None,
        title="Experiência base",
        description="Experiência base do Pokémon.",
        examples=[112]
    )
    hp: int = Field(
        ...,
        title="HP",
        description="Quantidade de HP do Pokémon.",
        examples=[35]
    )
    attack: int = Field(
        ...,
        title="Ataque",
        description="Valor de ataque do Pokémon.",
        examples=[55]
    )
    defense: int = Field(
        ...,
        title="Defesa",
        description="Valor de defesa do Pokémon.",
        examples=[40]
    )
    special_attack: int = Field(
        ...,
        title="Ataque especial",
        description="Valor de ataque especial do Pokémon.",
        examples=[50]
    )
    special_defense: int = Field(
        ...,
        title="Defesa especial",
        description="Valor de defesa especial do Pokémon.",
        examples=[50]
    )
    speed: int = Field(
        ...,
        title="Velocidade",
        description="Valor de velocidade do Pokémon.",
        examples=[90]
    )


class PokemonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        title="ID interno",
        description="Identificador interno do Pokémon no banco."
    )
    pokeapi_id: int = Field(
        ...,
        title="ID da PokéAPI",
        description="Identificador original do Pokémon na PokéAPI."
    )
    name: str = Field(
        ...,
        title="Nome",
        description="Nome do Pokémon."
    )
    type_1: str = Field(
        ...,
        title="Tipo principal",
        description="Tipo principal do Pokémon."
    )
    type_2: str | None = Field(
        default=None,
        title="Tipo secundário",
        description="Tipo secundário do Pokémon, se existir."
    )
    height: int = Field(
        ...,
        title="Altura",
        description="Altura do Pokémon."
    )
    weight: int = Field(
        ...,
        title="Peso",
        description="Peso do Pokémon."
    )
    base_experience: int | None = Field(
        default=None,
        title="Experiência base",
        description="Experiência base do Pokémon."
    )
    hp: int = Field(
        ...,
        title="HP",
        description="Quantidade de HP do Pokémon."
    )
    attack: int = Field(
        ...,
        title="Ataque",
        description="Valor de ataque do Pokémon."
    )
    defense: int = Field(
        ...,
        title="Defesa",
        description="Valor de defesa do Pokémon."
    )
    special_attack: int = Field(
        ...,
        title="Ataque especial",
        description="Valor de ataque especial do Pokémon."
    )
    special_defense: int = Field(
        ...,
        title="Defesa especial",
        description="Valor de defesa especial do Pokémon."
    )
    speed: int = Field(
        ...,
        title="Velocidade",
        description="Valor de velocidade do Pokémon."
    )

class PokemonListResponse(BaseModel):
    total: int = Field(
        ...,
        title="Total",
        description="Quantidade total de Pokémon encontrados."
    )
    limit: int = Field(
        ...,
        title="Limite",
        description="Quantidade máxima de registros retornados."
    )
    offset: int = Field(
        ...,
        title="Offset",
        description="Quantidade de registros ignorados antes da resposta."
    )
    items: list[PokemonResponse] = Field(
        ...,
        title="Itens",
        description="Lista de Pokémon retornados."
    )


class PokemonGenerationLoadResponse(BaseModel):
    generation_id: int = Field(
        ...,
        title="Geração",
        description="Geração carregada a partir da PokéAPI."
    )
    total_species: int = Field(
        ...,
        title="Total de espécies",
        description="Quantidade total de espécies encontradas na geração."
    )
    created_count: int = Field(
        ...,
        title="Criados",
        description="Quantidade de Pokémon novos salvos no banco."
    )
    existing_count: int = Field(
        ...,
        title="Já existentes",
        description="Quantidade de Pokémon que já estavam cadastrados."
    )
    skipped_count: int = Field(
        ...,
        title="Ignorados",
        description="Quantidade de Pokémon que não puderam ser carregados."
    )
    skipped_pokemon: list[str] = Field(
        ...,
        title="Pokémon ignorados",
        description="Nomes que falharam durante a carga."
    )
    items: list[PokemonResponse] = Field(
        ...,
        title="Pokémon carregados",
        description="Pokémon criados ou já existentes encontrados durante a carga."
    )

class TypeStatsResponse(BaseModel):
    type: str = Field(
        ...,
        title="Tipo",
        description="Tipo principal do grupo."
    )
    total_pokemon: int = Field(
        ...,
        title="Total de Pokémon",
        description="Quantidade de Pokémon com esse tipo principal."
    )
    average_hp: float = Field(
        ...,
        title="Média de vida",
        description="Média de vida dos Pokémon desse tipo."
    )
    average_attack: float = Field(
        ...,
        title="Média de ataque",
        description="Média de ataque dos Pokémon desse tipo."
    )
    average_special_attack: float = Field(
        ...,
        title="Média de ataque especial",
        description="Média de ataque especial dos Pokémon desse tipo."
    )
    average_defense: float = Field(
        ...,
        title="Média de defesa",
        description="Média de defesa dos Pokémon desse tipo."
    )
    average_special_defense: float = Field(
        ...,
        title="Média de defesa especial",
        description="Média de defesa especial dos Pokémon desse tipo."
    )
    average_speed: float = Field(
        ...,
        title="Média de velocidade",
        description="Média de velocidade dos Pokémon desse tipo."
    )

class StatsSummaryResponse(BaseModel):
    total_pokemon: int = Field(
        ...,
        title="Total de Pokémon",
        description="Quantidade total de Pokémon cadastrados no banco."
    )
    average_hp: float = Field(
        ...,
        title="Média de HP",
        description="Média geral de HP."
    )
    average_attack: float = Field(
        ...,
        title="Média de ataque",
        description="Média geral de ataque."
    )
    average_special_attack: float = Field(
        ...,
        title="Média de ataque especial",
        description="Média geral de ataque especial."
    )
    average_defense: float = Field(
        ...,
        title="Média de defesa",
        description="Média geral de defesa."
    )
    average_special_defense: float = Field(
        ...,
        title="Média de defesa especial",
        description="Média geral de defesa especial."
    )
    average_speed: float = Field(
        ...,
        title="Média de velocidade",
        description="Média geral de velocidade."
    )
    average_height: float = Field(
        ...,
        title="Média de altura",
        description="Média geral de altura."
    )
    average_weight: float = Field(
        ...,
        title="Média de peso",
        description="Média geral de peso."
    )

class TeamTypeEffectResponse(BaseModel):
    type: str = Field(
        ...,
        title="Tipo",
        description="Tipo ofensivo considerado na análise."
    )
    count: int = Field(
        ...,
        title="Quantidade afetada",
        description="Quantidade de Pokémon do time afetados por esse tipo."
    )
    pokemon: list[str] = Field(
        ...,
        title="Pokémon afetados",
        description="Lista dos Pokémon do time afetados por esse tipo."
    )
    average_multiplier: float = Field(
        ...,
        title="Multiplicador médio",
        description="Multiplicador médio de dano para os Pokémon afetados."
    )


class TeamAnalyzeRequest(BaseModel):
    team: list[str] = Field(
        ...,
        title="Time",
        description="Lista com os nomes dos Pokémon do time. Máximo de 6.",
        min_length=1,
        max_length=6,
        examples=[["charizard", "gyarados", "pikachu"]]
    )


class TeamAnalyzeResponse(BaseModel):
    team_size: int = Field(
        ...,
        title="Tamanho do time",
        description="Quantidade de Pokémon encontrados no banco."
    )
    pokemon_found: list[PokemonResponse] = Field(
        ...,
        title="Pokémon encontrados",
        description="Lista dos Pokémon encontrados para análise."
    )
    missing_pokemon: list[str] = Field(
        ...,
        title="Pokémon não encontrados",
        description="Nomes que não foram encontrados no banco."
    )
    types_present: list[str] = Field(
        ...,
        title="Tipos presentes",
        description="Todos os tipos presentes no time."
    )
    duplicate_types: list[str] = Field(
        ...,
        title="Tipos repetidos",
        description="Tipos que aparecem mais de uma vez no time."
    )
    weaknesses: list[TeamTypeEffectResponse] = Field(
        ...,
        title="Fraquezas",
        description="Tipos que causam dano aumentado a membros do time."
    )
    resistances: list[TeamTypeEffectResponse] = Field(
        ...,
        title="Resistências",
        description="Tipos que causam dano reduzido a membros do time."
    )
    immunities: list[TeamTypeEffectResponse] = Field(
        ...,
        title="Imunidades",
        description="Tipos que não causam dano a membros do time."
    )
    average_hp: float = Field(..., title="Média de HP")
    average_attack: float = Field(..., title="Média de ataque")
    average_special_attack: float = Field(..., title="Média de ataque especial")
    average_defense: float = Field(..., title="Média de defesa")
    average_special_defense: float = Field(..., title="Média de defesa especial")
    average_speed: float = Field(..., title="Média de velocidade")
    total_attack: int = Field(..., title="Ataque total")
    total_defense: int = Field(..., title="Defesa total")
    total_speed: int = Field(..., title="Velocidade total")

class TeamTypeSummaryResponse(BaseModel):
    tipo: str = Field(..., title="Tipo")
    quantidade: int = Field(..., title="Quantidade")


class TeamStatsSummaryResponse(BaseModel):
    hp: float = Field(..., title="HP")
    attack: float = Field(..., title="Ataque")
    special_attack: float = Field(..., title="Ataque especial")
    defense: float = Field(..., title="Defesa")
    special_defense: float = Field(..., title="Defesa especial")
    speed: float = Field(..., title="Velocidade")


class TeamAnalyzeSimpleResponse(BaseModel):
    team_size: int = Field(..., title="Tamanho do time")
    tipos_presentes: list[str] = Field(..., title="Tipos presentes")
    tipos_repetidos: list[str] = Field(..., title="Tipos repetidos")
    principais_fraquezas: list[TeamTypeSummaryResponse] = Field(..., title="Principais fraquezas")
    principais_resistencias: list[TeamTypeSummaryResponse] = Field(..., title="Principais resistências")
    imunidades: list[TeamTypeSummaryResponse] = Field(..., title="Imunidades")
    media_stats: TeamStatsSummaryResponse = Field(..., title="Média dos stats")
