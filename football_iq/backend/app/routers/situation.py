"""Situation Chart API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request

from app.auth import get_fabric_token_obo
from app.models.situation import Game, SituationChart, Team
from app.services.situation_chart import (
    get_games_between_teams,
    get_situation_chart,
    get_situation_chart_avg,
    get_teams,
)

router = APIRouter(prefix="/api/situation-chart", tags=["Situation Chart"])


@router.get("/teams", response_model=list[Team])
def list_teams(request: Request):
    """Return all NFL teams for the team selector."""
    token = get_fabric_token_obo(request)
    return get_teams(token)


@router.get("/games", response_model=list[Game])
def list_games(
    request: Request,
    my_team: str = Query(..., description="Your team abbreviation (e.g. SEA)"),
    opponent: str = Query(..., description="Opponent team abbreviation (e.g. SF)"),
    seasons_back: int = Query(2, description="Number of seasons to look back"),
):
    """Return games between two teams in recent seasons."""
    token = get_fabric_token_obo(request)
    from datetime import date

    current_year = date.today().year
    min_season = current_year - seasons_back
    return get_games_between_teams(token, my_team, opponent, min_season)


@router.get("/game", response_model=SituationChart)
def game_situation_chart(
    request: Request,
    game_key: str = Query(..., description="Game key (e.g. 2025_20_SF_SEA)"),
    offense_team: str = Query(..., description="Offense team abbreviation"),
):
    """Return situation chart for a specific game and offense."""
    token = get_fabric_token_obo(request)
    return get_situation_chart(token, game_key, offense_team)


@router.get("/average", response_model=SituationChart)
def average_situation_chart(
    request: Request,
    my_team: str = Query(..., description="Your team abbreviation"),
    opponent: str = Query(..., description="Opponent team abbreviation"),
    seasons_back: int = Query(2, description="Number of seasons to look back"),
):
    """Return average situation chart across all games between two teams."""
    token = get_fabric_token_obo(request)
    from datetime import date

    current_year = date.today().year
    min_season = current_year - seasons_back
    return get_situation_chart_avg(token, my_team, opponent, min_season)
