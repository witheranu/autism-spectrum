"use client";

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

interface AccuracyChartProps {
  data: { name: string; F1: number; Precision: number }[];
}

export function AccuracyChart({ data }: AccuracyChartProps) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="name" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
        <Tooltip cursor={{ fill: 'rgba(0,0,0,0.05)' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
        <Legend wrapperStyle={{ paddingTop: '10px' }} />
        <Bar dataKey="F1" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        <Bar dataKey="Precision" fill="#93c5fd" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
