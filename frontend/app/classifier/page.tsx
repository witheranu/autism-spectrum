import { getClassifierResults } from "@/lib/api";
import { ConfusionMatrix } from "@/components/charts/ConfusionMatrix";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { SeverityTier } from "@/lib/types";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

// Client component wrapper for Recharts
import { AccuracyChart } from "@/components/charts/AccuracyChart";

export const dynamic = "force-dynamic";


function calculateMetrics(data: { trueLabel: string; predictedLabel: string }[]) {
  const tiers = ["non_autistic", "autistic_tier_1", "autistic_tier_2", "autistic_tier_3"];
  const metrics: Record<string, { tp: number, fp: number, fn: number }> = {};
  
  tiers.forEach(t => metrics[t] = { tp: 0, fp: 0, fn: 0 });

  let correct = 0;
  data.forEach(d => {
    if (d.trueLabel === d.predictedLabel) {
      metrics[d.trueLabel].tp++;
      correct++;
    } else {
      if (metrics[d.predictedLabel]) metrics[d.predictedLabel].fp++;
      if (metrics[d.trueLabel]) metrics[d.trueLabel].fn++;
    }
  });

  const accuracy = correct / data.length;
  
  const perTier = tiers.map(t => {
    const { tp, fp, fn } = metrics[t];
    const precision = tp + fp === 0 ? 0 : tp / (tp + fp);
    const recall = tp + fn === 0 ? 0 : tp / (tp + fn);
    const f1 = precision + recall === 0 ? 0 : 2 * (precision * recall) / (precision + recall);
    
    return {
      tier: t,
      precision,
      recall,
      f1
    };
  });

  return { accuracy, perTier };
}

function formatLabel(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
}

export default async function ClassifierPage() {
  const results = await getClassifierResults();
  
  const { accuracy, perTier } = calculateMetrics(results);

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Classifier Results</h1>
        <p className="text-muted-foreground">
          Evaluation of the system's ability to blindly detect persona severity tiers from behavioral features.
        </p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-1 md:col-span-2 lg:col-span-1">
          <CardHeader>
            <CardTitle>Confusion Matrix</CardTitle>
            <CardDescription>Predicted vs True Persona Labels</CardDescription>
          </CardHeader>
          <CardContent>
            <ConfusionMatrix data={results} />
          </CardContent>
        </Card>

        <Card className="col-span-1 md:col-span-2 lg:col-span-1">
          <CardHeader>
            <CardTitle>Accuracy & F1 Scores</CardTitle>
            <CardDescription>Overall Accuracy: {(accuracy * 100).toFixed(1)}%</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <AccuracyChart data={perTier.map(t => ({
              name: formatLabel(t.tier).replace("Autistic ", ""),
              F1: t.f1 * 100,
              Precision: t.precision * 100
            }))} />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Per-Tier Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Severity Tier</TableHead>
                <TableHead className="text-right">Precision</TableHead>
                <TableHead className="text-right">Recall</TableHead>
                <TableHead className="text-right">F1 Score</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {perTier.map((t) => (
                <TableRow key={t.tier}>
                  <TableCell className="font-medium">{formatLabel(t.tier)}</TableCell>
                  <TableCell className="text-right">{(t.precision * 100).toFixed(1)}%</TableCell>
                  <TableCell className="text-right">{(t.recall * 100).toFixed(1)}%</TableCell>
                  <TableCell className="text-right">{(t.f1 * 100).toFixed(1)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
