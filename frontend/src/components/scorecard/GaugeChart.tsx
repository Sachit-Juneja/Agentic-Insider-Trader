"use client";

import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

interface GaugeChartProps {
  score: number;
  label?: string;
}

export function GaugeChart({ score, label = "Final Score" }: GaugeChartProps) {
  const data = [
    { name: "Score", value: score },
    { name: "Remaining", value: 100 - score },
  ];

  // Determine color based on score
  let color = "#00ff88"; // Green (Strong Buy)
  if (score < 25) color = "#ff3366"; // Red (Strong Sell)
  else if (score < 40) color = "#ff6b35"; // Orange (Sell)
  else if (score < 60) color = "#ffaa00"; // Yellow (Hold)
  else if (score < 75) color = "#00cc88"; // Light Green (Buy)

  return (
    <div className="flex flex-col items-center justify-center relative h-48">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="70%"
            startAngle={180}
            endAngle={0}
            innerRadius="60%"
            outerRadius="80%"
            paddingAngle={0}
            dataKey="value"
            stroke="none"
          >
            <Cell fill={color} className="drop-shadow-[0_0_8px_rgba(0,0,0,0.5)]" />
            <Cell fill="#1e293b" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      
      <div className="absolute flex flex-col items-center top-[55%]">
        <span className="text-4xl font-black tracking-tighter" style={{ color }}>
          {score.toFixed(1)}
        </span>
        <span className="text-xs uppercase tracking-widest text-slate-500 font-bold mt-1">
          {label}
        </span>
      </div>
    </div>
  );
}
