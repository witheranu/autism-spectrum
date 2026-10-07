"use client";

import { useState } from "react";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { Badge } from "@/components/ui/badge";

interface FeatureRadarChartProps {
  data: {
    subject: string;
    non_autistic: number;
    autistic_tier_1: number;
    autistic_tier_2: number;
    autistic_tier_3: number;
  }[];
}

export function FeatureRadarChart({ data }: FeatureRadarChartProps) {
  const [activeTiers, setActiveTiers] = useState({
    non_autistic: true,
    autistic_tier_1: true,
    autistic_tier_2: true,
    autistic_tier_3: true,
  });

  const toggleTier = (tier: keyof typeof activeTiers) => {
    setActiveTiers(prev => ({ ...prev, [tier]: !prev[tier] }));
  };

  const colors = {
    non_autistic: "#94a3b8", // Slate 400
    autistic_tier_1: "#93c5fd", // Blue 300
    autistic_tier_2: "#3b82f6", // Blue 500
    autistic_tier_3: "#1d4ed8", // Blue 700
  };

  return (
    <div className="flex flex-col space-y-4">
      <div className="flex flex-wrap gap-2 justify-center mb-4">
        {Object.entries(activeTiers).map(([tier, isActive]) => (
          <Badge 
            key={tier}
            variant={isActive ? "default" : "outline"}
            className="cursor-pointer select-none transition-all"
            onClick={() => toggleTier(tier as keyof typeof activeTiers)}
            style={isActive ? { backgroundColor: colors[tier as keyof typeof colors], color: tier === 'non_autistic' || tier === 'autistic_tier_1' ? '#0f172a' : '#ffffff' } : {}}
          >
            {tier.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())}
          </Badge>
        ))}
      </div>
      
      <div className="h-[400px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
            <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            
            {activeTiers.non_autistic && (
              <Radar name="Non Autistic" dataKey="non_autistic" stroke={colors.non_autistic} fill={colors.non_autistic} fillOpacity={0.2} />
            )}
            {activeTiers.autistic_tier_1 && (
              <Radar name="Tier 1" dataKey="autistic_tier_1" stroke={colors.autistic_tier_1} fill={colors.autistic_tier_1} fillOpacity={0.2} />
            )}
            {activeTiers.autistic_tier_2 && (
              <Radar name="Tier 2" dataKey="autistic_tier_2" stroke={colors.autistic_tier_2} fill={colors.autistic_tier_2} fillOpacity={0.2} />
            )}
            {activeTiers.autistic_tier_3 && (
              <Radar name="Tier 3" dataKey="autistic_tier_3" stroke={colors.autistic_tier_3} fill={colors.autistic_tier_3} fillOpacity={0.2} />
            )}
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
