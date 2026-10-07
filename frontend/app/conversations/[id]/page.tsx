import { getConversation, getClassifierResults } from "@/lib/api";
import { ConversationBubble } from "@/components/ConversationBubble";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SeverityTier } from "@/lib/types";
import { notFound } from "next/navigation";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

export const dynamic = "force-dynamic";

function getTierColor(tier: SeverityTier) {
  switch (tier) {
    case "non_autistic": return "bg-[var(--color-tier-0)] text-slate-800";
    case "autistic_tier_1": return "bg-[var(--color-tier-1)] text-slate-900";
    case "autistic_tier_2": return "bg-[var(--color-tier-2)] text-white";
    case "autistic_tier_3": return "bg-[var(--color-tier-3)] text-white";
    default: return "bg-gray-100";
  }
}

function formatLabel(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
}

export default async function ConversationViewer({ params }: { params: Promise<{ id: string }> | { id: string } }) {
  const resolvedParams = await Promise.resolve(params);
  const [conversation, classifierResults] = await Promise.all([
    getConversation(resolvedParams.id),
    getClassifierResults(),
  ]);

  if (!conversation) {
    notFound();
  }

  // Assume the "ground truth" we are predicting is for Agent B in this simulation
  const result = classifierResults.find(r => r.conversationId === resolvedParams.id);
  const targetAgent = conversation.agentB; // Typically the one being classified
  const trueLabel = targetAgent.label;
  const predictedLabel = result?.predictedLabel;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Link href="/conversations" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground">
        <ChevronLeft className="mr-1 h-4 w-4" />
        Back to Conversations
      </Link>

      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{conversation.scenario}</h1>
          <p className="text-muted-foreground">ID: {conversation.id}</p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <Card className="flex-1">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Ground Truth Persona</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-lg">{targetAgent.id}</span>
                <Badge variant="outline" className={getTierColor(trueLabel)}>
                  {formatLabel(trueLabel)}
                </Badge>
              </div>
              <div className="text-sm mt-1 text-muted-foreground">
                Traits: {targetAgent.traits.join(", ")}
              </div>
            </CardContent>
          </Card>

          {result && (
            <Card className="flex-1">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Classifier Prediction</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className={getTierColor(predictedLabel!)}>
                    {formatLabel(predictedLabel!)}
                  </Badge>
                </div>
                <div className="text-sm mt-1 text-muted-foreground">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Transcript</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col space-y-2">
            {conversation.turns.map((turn, idx) => (
              <ConversationBubble
                key={idx}
                text={turn.text}
                speaker={turn.speaker}
                isCurrentUser={turn.speaker === conversation.agentA.id}
                timestamp={turn.timestamp}
              />
            ))}
          </div>
        </CardContent>
      </Card>
      
      {conversation.interview.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Post-Conversation Interview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
             {conversation.interview.map((qna, idx) => (
               <div key={idx} className="space-y-1">
                 <p className="font-medium text-sm">Q: {qna.question}</p>
                 <p className="text-sm text-muted-foreground">A: {qna.answer}</p>
               </div>
             ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
