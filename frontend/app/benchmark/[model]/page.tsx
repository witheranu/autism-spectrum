import { getBenchmarkResults } from "@/lib/api";
import { notFound } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AnnotatedTranscript } from "@/components/AnnotatedTranscript";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function ModelDrillDownPage({ params }: { params: Promise<{ model: string }> | { model: string } }) {
  const resolvedParams = await Promise.resolve(params);
  const modelName = decodeURIComponent(resolvedParams.model);
  const results = await getBenchmarkResults();
  const entry = results.find(r => r.model === modelName);

  if (!entry) {
    notFound();
  }

  // Mocking an annotated transcript for demonstration purposes
  const dummySpans: {text: string, framing: "deficit" | "strength" | "neutral"}[] = [
    { text: "The candidate", framing: "neutral" },
    { text: "struggles with basic social cues", framing: "deficit" },
    { text: "and", framing: "neutral" },
    { text: "fails to maintain appropriate eye contact", framing: "deficit" },
    { text: "during the interview.", framing: "neutral" },
    { text: "However, they demonstrated an", framing: "neutral" },
    { text: "exceptional attention to detail", framing: "strength" },
    { text: "and", framing: "neutral" },
    { text: "deep focus on complex technical problems.", framing: "strength" },
    { text: "We should provide", framing: "neutral" },
    { text: "clear written instructions", framing: "strength" },
    { text: "instead of relying on verbal ambiguity.", framing: "neutral" }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <Link href="/benchmark" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground">
        <ChevronLeft className="mr-1 h-4 w-4" />
        Back to Leaderboard
      </Link>

      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">{entry.model}</h1>
        <p className="text-muted-foreground">Detailed bias analysis and annotated transcripts.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Overall Score: {entry.overallScore}/100</CardTitle>
            <CardDescription>Scenario: {entry.scenario}</CardDescription>
          </CardHeader>
        </Card>

        {entry.biasScores.map((score, idx) => (
          <Card key={idx}>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg capitalize">{score.dimension.replace('_', ' ')}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold mb-2">{score.score}</div>
              <p className="text-sm text-muted-foreground">{score.justification}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Annotated Output Example</CardTitle>
          <CardDescription>
            Color-coded spans highlighting framing types. 
            <span className="inline-block ml-4 px-2 py-0.5 bg-[var(--color-frame-deficit)]/40 text-red-900 rounded-sm text-xs">Deficit</span>
            <span className="inline-block ml-2 px-2 py-0.5 bg-[var(--color-frame-strength)]/60 text-green-900 rounded-sm text-xs">Strength</span>
            <span className="inline-block ml-2 px-2 py-0.5 bg-[var(--color-frame-neutral)]/20 rounded-sm text-xs">Neutral</span>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <AnnotatedTranscript spans={dummySpans} />
        </CardContent>
      </Card>
    </div>
  );
}
