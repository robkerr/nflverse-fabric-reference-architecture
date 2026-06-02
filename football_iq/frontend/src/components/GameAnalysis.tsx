"use client";

import { useState, useEffect } from "react";
import { useMsal, useIsAuthenticated } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import { useApi } from "../hooks/useApi";
import { Team, Game, SituationChart } from "../types";
import SituationChartTable from "./SituationChartTable";

export default function GameAnalysis() {
  const { instance } = useMsal();
  const isAuthenticated = useIsAuthenticated();
  const { apiFetch } = useApi();

  const [teams, setTeams] = useState<Team[]>([]);
  const [myTeam, setMyTeam] = useState("");
  const [opponent, setOpponent] = useState("");
  const [games, setGames] = useState<Game[]>([]);
  const [selectedGame, setSelectedGame] = useState("");
  const [chartData, setChartData] = useState<SituationChart | null>(null);
  const [avgData, setAvgData] = useState<SituationChart | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load teams on auth
  useEffect(() => {
    if (!isAuthenticated) return;
    apiFetch<Team[]>("/api/situation-chart/teams")
      .then(setTeams)
      .catch((e) => setError(e.message));
  }, [isAuthenticated]);

  // Load games when both teams selected
  useEffect(() => {
    if (!myTeam || !opponent || myTeam === opponent) {
      setGames([]);
      setSelectedGame("");
      setChartData(null);
      setAvgData(null);
      return;
    }

    setLoading(true);
    setError("");
    Promise.all([
      apiFetch<Game[]>("/api/situation-chart/games", {
        my_team: myTeam,
        opponent: opponent,
        seasons_back: "2",
      }),
      apiFetch<SituationChart>("/api/situation-chart/average", {
        my_team: myTeam,
        opponent: opponent,
        seasons_back: "2",
      }),
    ])
      .then(([gamesData, avg]) => {
        setGames(gamesData);
        setAvgData(avg);
        setSelectedGame("");
        setChartData(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [myTeam, opponent]);

  // Load situation chart for selected game
  useEffect(() => {
    if (!selectedGame || !myTeam) return;

    setLoading(true);
    setError("");
    apiFetch<SituationChart>("/api/situation-chart/game", {
      game_key: selectedGame,
      offense_team: myTeam,
    })
      .then(setChartData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [selectedGame]);

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4">
        <h1 className="text-3xl font-bold">Football IQ</h1>
        <p className="text-gray-400">Sign in to analyze game situations</p>
        <button
          onClick={() => instance.loginPopup(loginRequest)}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          Sign in with Microsoft
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Football IQ — Situation Chart</h1>
        <button
          onClick={() => instance.logoutPopup()}
          className="text-sm text-gray-400 hover:text-white"
        >
          Sign out
        </button>
      </div>

      {error && (
        <div className="bg-red-900/50 border border-red-500 rounded p-3 text-red-200">
          {error}
        </div>
      )}

      {/* Team Selectors */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">My Team</label>
          <select
            value={myTeam}
            onChange={(e) => setMyTeam(e.target.value)}
            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
          >
            <option value="">Select team...</option>
            {teams.map((t) => (
              <option key={t.team_key} value={t.team_key}>
                {t.team_name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Opponent</label>
          <select
            value={opponent}
            onChange={(e) => setOpponent(e.target.value)}
            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
          >
            <option value="">Select opponent...</option>
            {teams
              .filter((t) => t.team_key !== myTeam)
              .map((t) => (
                <option key={t.team_key} value={t.team_key}>
                  {t.team_name}
                </option>
              ))}
          </select>
        </div>
      </div>

      {/* Game Selector */}
      {games.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Select Game ({games.length} matchups found)
          </label>
          <select
            value={selectedGame}
            onChange={(e) => setSelectedGame(e.target.value)}
            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
          >
            <option value="">Select a game...</option>
            {games.map((g) => (
              <option key={g.game_key} value={g.game_key}>
                {g.game_date} — {g.away_team} @ {g.home_team} ({g.away_score}-{g.home_score})
              </option>
            ))}
          </select>
        </div>
      )}

      {loading && <p className="text-gray-400 animate-pulse">Loading...</p>}

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {chartData && (
          <SituationChartTable
            data={chartData}
            title={`${myTeam} Offense — Game`}
          />
        )}
        {avgData && (
          <SituationChartTable
            data={avgData}
            title={`${myTeam} vs ${opponent} — Avg/Game`}
          />
        )}
      </div>
    </div>
  );
}
