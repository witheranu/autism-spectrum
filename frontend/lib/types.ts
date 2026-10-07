export type SeverityTier = "non_autistic" | "autistic_tier_1" | "autistic_tier_2" | "autistic_tier_3";

export interface Persona {
  id: string;
  label: SeverityTier;
  traits: string[];
}

export interface ConversationTurn {
  speaker: string; // usually Persona ID or Name
  text: string;
  timestamp: string;
}

export interface InterviewQnA {
  question: string;
  answer: string;
}

export interface Conversation {
  id: string;
  scenario: string;
  agentA: Persona;
  agentB: Persona;
  turns: ConversationTurn[];
  interview: InterviewQnA[];
}

export interface ClassifierResult {
  conversationId: string;
  trueLabel: SeverityTier;
  predictedLabel: SeverityTier;
  confidence: number;
  features: Record<string, number>;
}

export interface BiasScore {
  dimension: string; // e.g., "deficit_framing", "stereotype_presence"
  score: number; // typically 0-100 or 0-1
  justification: string;
}

export interface BenchmarkEntry {
  model: string;
  scenario: string;
  biasScores: BiasScore[];
  overallScore: number;
}
