"""Pydantic models for the Situation Chart API responses."""

from __future__ import annotations

from pydantic import BaseModel


class Team(BaseModel):
    team_key: str
    team_name: str
    team_nick: str
    team_conf: str
    team_division: str


class Game(BaseModel):
    game_key: str
    game_date: str
    season: int
    week: int
    game_type: str
    home_team: str
    away_team: str
    home_score: int | None
    away_score: int | None
    winning_team: str | None
    stadium: str | None


class SituationChart(BaseModel):
    first_and_10: int
    second_down: int
    second_short: int
    second_medium: int
    second_long: int
    third_down: int
    third_short: int
    third_medium: int
    third_long: int
    backed_up: int
    red_zone: int
    high_red_zone: int
    low_red_zone: int
    goal_line: int
    total_plays: int
    games_averaged: int | None = None
