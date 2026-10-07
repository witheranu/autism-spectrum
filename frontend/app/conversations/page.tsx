import { getConversations } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { SeverityTier } from "@/lib/types";

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

export default async function ConversationsPage() {
  const conversations = await getConversations();

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Conversations</h1>
        <p className="text-muted-foreground">
          Browse the simulated multi-agent interactions across different severity tiers.
        </p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {conversations.map((conv) => (
          <Link key={conv.id} href={`/conversations/${conv.id}`}>
            <Card className="hover:bg-muted/50 transition-colors h-full cursor-pointer">
              <CardHeader>
                <CardTitle className="text-lg">{conv.scenario}</CardTitle>
                <CardDescription>ID: {conv.id}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-center text-sm">
                      <span className="font-medium">{conv.agentA.id}</span>
                      <Badge variant="outline" className={getTierColor(conv.agentA.label)}>
                        {formatLabel(conv.agentA.label)}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="font-medium">{conv.agentB.id}</span>
                      <Badge variant="outline" className={getTierColor(conv.agentB.label)}>
                        {formatLabel(conv.agentB.label)}
                      </Badge>
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {conv.turns.length} turns
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
