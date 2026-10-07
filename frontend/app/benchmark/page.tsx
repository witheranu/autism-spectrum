import { getBenchmarkResults } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { LeaderboardBarChart } from "@/components/charts/LeaderboardBarChart";
import Link from "next/link";
import { Button, buttonVariants } from "@/components/ui/button";

export const dynamic = "force-dynamic";


export default async function BenchmarkPage() {
  const results = await getBenchmarkResults();

  const chartData = results.map(entry => {
    const dataPoint: any = { model: entry.model };
    entry.biasScores.forEach(score => {
      dataPoint[score.dimension] = score.score;
    });
    return dataPoint;
  });

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Benchmark Leaderboard</h1>
        <p className="text-muted-foreground">
          Compare LLMs across various bias dimensions in multi-agent simulation scenarios.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Bias Dimensions Comparison</CardTitle>
          <CardDescription>Grouped bar chart showing scores per model.</CardDescription>
        </CardHeader>
        <CardContent className="h-[400px]">
          <LeaderboardBarChart data={chartData} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Leaderboard</CardTitle>
          <CardDescription>Models sorted by overall performance score (higher is better).</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Model</TableHead>
                <TableHead>Scenario</TableHead>
                <TableHead className="text-right">Overall Score</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {results.sort((a, b) => b.overallScore - a.overallScore).map(entry => (
                <TableRow key={entry.model}>
                  <TableCell className="font-medium">{entry.model}</TableCell>
                  <TableCell>{entry.scenario}</TableCell>
                  <TableCell className="text-right font-semibold">{entry.overallScore}/100</TableCell>
                  <TableCell className="text-right">
                    <Link href={`/benchmark/${encodeURIComponent(entry.model)}`} className={buttonVariants({ variant: "outline", size: "sm" })}>
                      Drill Down
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
