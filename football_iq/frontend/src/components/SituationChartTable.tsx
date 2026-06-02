"use client";

import { SituationChart } from "../types";

interface Props {
  data: SituationChart;
  title: string;
}

export default function SituationChartTable({ data, title }: Props) {
  const downRows = [
    { label: "1st & 10", value: data.first_and_10 },
    { label: "2nd Down", value: data.second_down },
    { label: "2nd & Short (1-2)", value: data.second_short },
    { label: "2nd & Medium (3-6)", value: data.second_medium },
    { label: "2nd & Long (7+)", value: data.second_long },
    { label: "3rd Down", value: data.third_down },
    { label: "3rd & Short (1-2)", value: data.third_short },
    { label: "3rd & Medium (3-6)", value: data.third_medium },
    { label: "3rd & Long (7+)", value: data.third_long },
  ];

  const situationRows = [
    { label: "Backed Up (-1 to -10)", value: data.backed_up },
    { label: "Red Zone", value: data.red_zone },
    { label: "High Red Zone (20-13)", value: data.high_red_zone },
    { label: "Low Red Zone (12-4)", value: data.low_red_zone },
    { label: "Goal Line (3-in)", value: data.goal_line },
  ];

  return (
    <div className="bg-gray-900 rounded-lg p-6 text-white">
      <h2 className="text-xl font-bold text-center mb-4 uppercase tracking-wide text-yellow-400">
        {title}
      </h2>
      <div className="grid grid-cols-2 gap-8">
        {/* Down & Distance column */}
        <div>
          <div className="grid grid-cols-[1fr_60px] gap-1 font-bold text-sm uppercase border-b border-gray-600 pb-1 mb-2">
            <span>Down and Distance</span>
            <span className="text-center">Count</span>
          </div>
          {downRows.map((row) => (
            <div
              key={row.label}
              className="grid grid-cols-[1fr_60px] gap-1 py-1 border-b border-gray-700 text-sm"
            >
              <span>{row.label}</span>
              <span className="text-center font-bold">{row.value}</span>
            </div>
          ))}
        </div>

        {/* Situation column */}
        <div>
          <div className="grid grid-cols-[1fr_60px] gap-1 font-bold text-sm uppercase border-b border-gray-600 pb-1 mb-2">
            <span>Situation</span>
            <span className="text-center">Count</span>
          </div>
          {situationRows.map((row) => (
            <div
              key={row.label}
              className="grid grid-cols-[1fr_60px] gap-1 py-1 border-b border-gray-700 text-sm"
            >
              <span>{row.label}</span>
              <span className="text-center font-bold">{row.value}</span>
            </div>
          ))}
          {/* Total */}
          <div className="grid grid-cols-[1fr_60px] gap-1 py-2 mt-4 border-t-2 border-yellow-400 font-bold text-sm">
            <span className="uppercase">Total Plays</span>
            <span className="text-center text-yellow-400">{data.total_plays}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
