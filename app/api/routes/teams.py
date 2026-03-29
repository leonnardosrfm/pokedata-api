from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    TeamAnalyzeRequest,
    TeamAnalyzeResponse,
    TeamAnalyzeSimpleResponse,
)
from app.services.team_service import (
    build_detailed_team_response,
    build_simple_team_response,
    get_team_base_data,
)

router = APIRouter(prefix="/teams", tags=["Times"])


@router.post(
    "/analyze",
    response_model=TeamAnalyzeSimpleResponse,
    summary="Analisar time",
    description="Retorna um resumo simplificado do time.",
    response_description="Resumo enxuto do time.",
)
def analyze_team(payload: TeamAnalyzeRequest, db: Session = Depends(get_db)):
    data = get_team_base_data(payload.team, db)
    return build_simple_team_response(data)


@router.post(
    "/analyze/detailed",
    response_model=TeamAnalyzeResponse,
    summary="Analisar time detalhadamente",
    description="Retorna a análise completa do time.",
    response_description="Resumo detalhado do time.",
)
def analyze_team_detailed(payload: TeamAnalyzeRequest, db: Session = Depends(get_db)):
    data = get_team_base_data(payload.team, db)
    return build_detailed_team_response(data)