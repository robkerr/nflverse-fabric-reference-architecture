export interface Team {
  team_key: string;
  team_name: string;
  team_nick: string;
  team_conf: string;
  team_division: string;
}

export interface Game {
  game_key: string;
  game_date: string;
  season: number;
  week: number;
  game_type: string;
  home_team: string;
  away_team: string;
  home_score: number | null;
  away_score: number | null;
  winning_team: string | null;
  stadium: string | null;
}

export interface SituationChart {
  first_and_10: number;
  second_down: number;
  second_short: number;
  second_medium: number;
  second_long: number;
  third_down: number;
  third_short: number;
  third_medium: number;
  third_long: number;
  backed_up: number;
  red_zone: number;
  high_red_zone: number;
  low_red_zone: number;
  goal_line: number;
  total_plays: number;
  games_averaged?: number | null;
}
