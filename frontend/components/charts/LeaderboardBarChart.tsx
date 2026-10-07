"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

interface LeaderboardBarChartProps {
  data: {
    model: string;
    deficit_framing: number;
    stereotype_presence: number;
    accommodation_asymmetry: number;
    agency_framing: number;
  }[];
}

export function LeaderboardBarChart({ data }: LeaderboardBarChartProps) {
  const colors = {
    deficit_framing: "#f43f5e", // Rose 500
    stereotype_presence: "#8b5cf6", // Violet 500
    accommodation_asymmetry: "#f59e0b", // Amber 500
    agency_framing: "#10b981", // Emerald 500
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="model" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis fontSize={12} tickLine={false} axisLine={false} />
        <Tooltip cursor={{ fill: 'rgba(0,0,0,0.05)' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
        <Legend wrapperStyle={{ paddingTop: '10px' }} />
        <Bar dataKey="deficit_framing" name="Deficit Framing" fill={colors.deficit_framing} radius={[4, 4, 0, 0]} />
        <Bar dataKey="stereotype_presence" name="Stereotype" fill={colors.stereotype_presence} radius={[4, 4, 0, 0]} />
        <Bar dataKey="accommodation_asymmetry" name="Asymmetry" fill={colors.accommodation_asymmetry} radius={[4, 4, 0, 0]} />
        <Bar dataKey="agency_framing" name="Agency" fill={colors.agency_framing} radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
