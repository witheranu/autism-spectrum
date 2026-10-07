"use client";

import { useMemo } from "react";
import { SeverityTier } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ConfusionMatrixProps {
  data: { trueLabel: SeverityTier; predictedLabel: SeverityTier }[];
}

const tiers: SeverityTier[] = [
  "non_autistic",
  "autistic_tier_1",
  "autistic_tier_2",
  "autistic_tier_3",
];

function formatLabel(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
}

export function ConfusionMatrix({ data }: ConfusionMatrixProps) {
  const matrix = useMemo(() => {
    const mat: Record<string, Record<string, number>> = {};
    tiers.forEach(t1 => {
      mat[t1] = {};
      tiers.forEach(t2 => {
        mat[t1][t2] = 0;
      });
    });

    let maxVal = 0;
    data.forEach(item => {
      if (mat[item.trueLabel] && mat[item.trueLabel][item.predictedLabel] !== undefined) {
        mat[item.trueLabel][item.predictedLabel]++;
        maxVal = Math.max(maxVal, mat[item.trueLabel][item.predictedLabel]);
      }
    });
    return { mat, maxVal: maxVal || 1 };
  }, [data]);

  return (
    <div className="overflow-x-auto pb-4">
      <div className="min-w-max">
        <div className="grid grid-cols-[150px_repeat(4,_minmax(100px,_1fr))] gap-1 text-sm">
          <div className="flex items-end justify-end p-2 font-medium text-muted-foreground">
            True \ Pred
          </div>
          {tiers.map(t => (
            <div key={`col-${t}`} className="text-center p-2 font-medium whitespace-nowrap overflow-hidden text-ellipsis" title={formatLabel(t)}>
              {formatLabel(t).replace("Autistic ", "")}
            </div>
          ))}
          
          {tiers.map(trueTier => (
            <div key={`row-${trueTier}`} className="contents">
              <div className="flex items-center justify-end p-2 font-medium whitespace-nowrap text-right pr-4 border-r">
                {formatLabel(trueTier)}
              </div>
              {tiers.map(predTier => {
                const count = matrix.mat[trueTier][predTier];
                const intensity = count / matrix.maxVal; // 0 to 1
                
                return (
                  <div 
                    key={`cell-${trueTier}-${predTier}`}
                    className="flex items-center justify-center h-12 rounded-sm transition-colors border"
                    style={{
                      backgroundColor: count > 0 ? `rgba(59, 130, 246, ${intensity * 0.8 + 0.1})` : 'transparent',
                      color: count > 0 && intensity > 0.5 ? 'white' : 'inherit'
                    }}
                    title={`True: ${formatLabel(trueTier)}\nPred: ${formatLabel(predTier)}\nCount: ${count}`}
                  >
                    {count}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
