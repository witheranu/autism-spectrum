"""
Pydantic V2 schemas for request / response validation.

Every "read" schema sets `model_config = ConfigDict(from_attributes=True)`
so it can be constructed directly from an ORM model instance.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Severity tier literal (used across schemas) ─────────────────────────────

# Keeping as a plain str for now; validation at the route level can
# constrain this to the four allowed values if needed.
SeverityTier = str  # "non_autistic" | "autistic_tier_1" | "autistic_tier_2" | "autistic_tier_3"


# ── Persona ──────────────────────────────────────────────────────────────────

class PersonaBase(BaseModel):
    label: SeverityTier
    traits: list[str] = []


class PersonaCreate(PersonaBase):
    pass


class PersonaRead(PersonaBase):
    model_config = ConfigDict(from_attributes=True)
    id: str


# ── ConversationTurn ─────────────────────────────────────────────────────────

class ConversationTurnBase(BaseModel):
    speaker: str
    text: str
    timestamp: datetime


class ConversationTurnCreate(ConversationTurnBase):
    pass


class ConversationTurnRead(ConversationTurnBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_id: str


# ── InterviewResponse ────────────────────────────────────────────────────────

class InterviewResponseBase(BaseModel):
    question: str
    answer: str


class InterviewResponseCreate(InterviewResponseBase):
    agent_id: str


class InterviewResponseRead(InterviewResponseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_id: str
    agent_id: str


# ── Conversation ─────────────────────────────────────────────────────────────

class ConversationBase(BaseModel):
    scenario: str


class ConversationCreate(ConversationBase):
    agent_a_id: str
    agent_b_id: str


class ConversationRead(ConversationBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    agent_a_id: str
    agent_b_id: str
    created_at: datetime
    agent_a: PersonaRead
    agent_b: PersonaRead
    turns: list[ConversationTurnRead] = []
    interview_responses: list[InterviewResponseRead] = []


class ConversationSummary(BaseModel):
    """Lighter projection used for listing conversations (no nested turns)."""
    model_config = ConfigDict(from_attributes=True)
    id: str
    scenario: str
    agent_a_id: str
    agent_b_id: str
    created_at: datetime
    agent_a: PersonaRead
    agent_b: PersonaRead


# ── ExtractedFeature ─────────────────────────────────────────────────────────

class ExtractedFeatureBase(BaseModel):
    feature_name: str
    value: float


class ExtractedFeatureCreate(ExtractedFeatureBase):
    conversation_id: str


class ExtractedFeatureRead(ExtractedFeatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_id: str


# ── ClassifierResult ─────────────────────────────────────────────────────────

class ClassifierResultBase(BaseModel):
    true_label: SeverityTier
    predicted_label: SeverityTier
    confidence: float


class ClassifierResultCreate(ClassifierResultBase):
    conversation_id: str


class ClassifierResultRead(ClassifierResultBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_id: str


# ── BenchmarkEntry ───────────────────────────────────────────────────────────

class BiasScoreRead(BaseModel):
    """Convenience shape matching the frontend's BiasScore type."""
    dimension: str
    score: float
    justification: str


class BenchmarkEntryBase(BaseModel):
    model_name: str
    scenario: str
    dimension: str
    score: float
    justification: str = ""


class BenchmarkEntryCreate(BenchmarkEntryBase):
    pass


class BenchmarkEntryRead(BenchmarkEntryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Health ───────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    environment: str
