import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button, buttonVariants } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <div className="text-center space-y-4 pt-12 pb-6">
        <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">
          Autism Bias Research Dashboard
        </h1>
        <p className="text-xl text-muted-foreground">
          A multi-agent simulation platform for studying implicit autism-related bias in Large Language Models.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Conversations</CardTitle>
            <CardDescription>View simulated multi-agent interactions</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Explore transcripts between non-autistic and autistic personas across different severity tiers.
            </p>
            <Link href="/conversations" className={buttonVariants({ variant: "default" })}>
              View Conversations
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Classifier Results</CardTitle>
            <CardDescription>Persona detection analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Analyze the confusion matrix and accuracy of the system trying to blindly detect persona severity tiers.
            </p>
            <Link href="/classifier" className={buttonVariants({ variant: "secondary" })}>
              View Classifier
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Feature Dashboard</CardTitle>
            <CardDescription>Behavioral divergence</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Analyze extracted features like literal interpretation and direct communication via radar charts.
            </p>
            <Link href="/features" className={buttonVariants({ variant: "secondary" })}>
              View Features
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Benchmark Leaderboard</CardTitle>
            <CardDescription>Compare LLM bias scores</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              See how different LLMs score on deficit framing, stereotype presence, and accommodation asymmetry.
            </p>
            <Link href="/benchmark" className={buttonVariants({ variant: "secondary" })}>
              View Leaderboard
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
