"""SQL queries for the Situation Chart feature."""

from __future__ import annotations

from typing import Any

from app.services.fabric_sql import execute_query

TEAMS_QUERY = """
SELECT team_key, team_name, team_nick, team_conf, team_division
FROM gold.dim_team
ORDER BY team_name
"""

GAMES_BETWEEN_TEAMS_QUERY = """
SELECT
    g.game_key,
    g.game_date,
    g.season,
    g.week,
    g.game_type,
    g.home_team,
    g.away_team,
    g.home_score,
    g.away_score,
    g.winning_team,
    g.stadium
FROM gold.dim_game g
WHERE g.season >= ?
  AND (
    (g.home_team = ? AND g.away_team = ?)
    OR (g.home_team = ? AND g.away_team = ?)
  )
ORDER BY g.game_date DESC
"""

SITUATION_CHART_QUERY = """
WITH plays AS (
    SELECT
        p.down,
        p.ydstogo,
        p.yardline_100
    FROM gold.fact_play_core p
    WHERE p.game_key = ?
      AND p.offense_team_key = ?
      AND p.play_type_group IN ('Dropback', 'Designed rush', 'QB scramble')
)
SELECT
    -- Down and distance
    SUM(CASE WHEN down = 1 AND ydstogo >= 9 AND ydstogo <= 11 THEN 1 ELSE 0 END) AS first_and_10,
    SUM(CASE WHEN down = 2 THEN 1 ELSE 0 END) AS second_down,
    SUM(CASE WHEN down = 2 AND ydstogo BETWEEN 1 AND 2 THEN 1 ELSE 0 END) AS second_short,
    SUM(CASE WHEN down = 2 AND ydstogo BETWEEN 3 AND 6 THEN 1 ELSE 0 END) AS second_medium,
    SUM(CASE WHEN down = 2 AND ydstogo >= 7 THEN 1 ELSE 0 END) AS second_long,
    SUM(CASE WHEN down = 3 THEN 1 ELSE 0 END) AS third_down,
    SUM(CASE WHEN down = 3 AND ydstogo BETWEEN 1 AND 2 THEN 1 ELSE 0 END) AS third_short,
    SUM(CASE WHEN down = 3 AND ydstogo BETWEEN 3 AND 6 THEN 1 ELSE 0 END) AS third_medium,
    SUM(CASE WHEN down = 3 AND ydstogo >= 7 THEN 1 ELSE 0 END) AS third_long,
    -- Field position situations
    SUM(CASE WHEN yardline_100 >= 90 THEN 1 ELSE 0 END) AS backed_up,
    SUM(CASE WHEN yardline_100 <= 20 THEN 1 ELSE 0 END) AS red_zone,
    SUM(CASE WHEN yardline_100 BETWEEN 13 AND 20 THEN 1 ELSE 0 END) AS high_red_zone,
    SUM(CASE WHEN yardline_100 BETWEEN 4 AND 12 THEN 1 ELSE 0 END) AS low_red_zone,
    SUM(CASE WHEN yardline_100 <= 3 THEN 1 ELSE 0 END) AS goal_line,
    COUNT(*) AS total_plays
FROM plays
"""

SITUATION_CHART_AVG_QUERY = """
WITH plays AS (
    SELECT
        p.down,
        p.ydstogo,
        p.yardline_100,
        p.game_key
    FROM gold.fact_play_core p
    INNER JOIN gold.dim_game g ON p.game_key = g.game_key
    WHERE p.offense_team_key = ?
      AND p.play_type_group IN ('Dropback', 'Designed rush', 'QB scramble')
      AND g.season >= ?
      AND (
        (g.home_team = ? AND g.away_team = ?)
        OR (g.home_team = ? AND g.away_team = ?)
      )
),
game_count AS (
    SELECT COUNT(DISTINCT game_key) AS num_games FROM plays
)
SELECT
    -- Down and distance (avg per game)
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 1 AND ydstogo >= 9 AND ydstogo <= 11 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS first_and_10,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 2 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS second_down,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 2 AND ydstogo BETWEEN 1 AND 2 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS second_short,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 2 AND ydstogo BETWEEN 3 AND 6 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS second_medium,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 2 AND ydstogo >= 7 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS second_long,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 3 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS third_down,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 3 AND ydstogo BETWEEN 1 AND 2 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS third_short,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 3 AND ydstogo BETWEEN 3 AND 6 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS third_medium,
    CAST(ROUND(1.0 * SUM(CASE WHEN down = 3 AND ydstogo >= 7 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS third_long,
    -- Field position (avg per game)
    CAST(ROUND(1.0 * SUM(CASE WHEN yardline_100 >= 90 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS backed_up,
    CAST(ROUND(1.0 * SUM(CASE WHEN yardline_100 <= 20 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS red_zone,
    CAST(ROUND(1.0 * SUM(CASE WHEN yardline_100 BETWEEN 13 AND 20 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS high_red_zone,
    CAST(ROUND(1.0 * SUM(CASE WHEN yardline_100 BETWEEN 4 AND 12 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS low_red_zone,
    CAST(ROUND(1.0 * SUM(CASE WHEN yardline_100 <= 3 THEN 1 ELSE 0 END) / MAX(gc.num_games), 0) AS INT) AS goal_line,
    CAST(ROUND(1.0 * COUNT(*) / MAX(gc.num_games), 0) AS INT) AS total_plays,
    MAX(gc.num_games) AS games_averaged
FROM plays
CROSS JOIN game_count gc
"""


def get_teams(access_token: str) -> list[dict[str, Any]]:
    return execute_query(access_token, TEAMS_QUERY)


def get_games_between_teams(
    access_token: str,
    team1: str,
    team2: str,
    min_season: int,
) -> list[dict[str, Any]]:
    return execute_query(
        access_token,
        GAMES_BETWEEN_TEAMS_QUERY,
        (min_season, team1, team2, team2, team1),
    )


def get_situation_chart(
    access_token: str,
    game_key: str,
    offense_team: str,
) -> dict[str, Any]:
    rows = execute_query(access_token, SITUATION_CHART_QUERY, (game_key, offense_team))
    return rows[0] if rows else {}


def get_situation_chart_avg(
    access_token: str,
    offense_team: str,
    opponent_team: str,
    min_season: int,
) -> dict[str, Any]:
    rows = execute_query(
        access_token,
        SITUATION_CHART_AVG_QUERY,
        (offense_team, min_season, offense_team, opponent_team, opponent_team, offense_team),
    )
    return rows[0] if rows else {}
