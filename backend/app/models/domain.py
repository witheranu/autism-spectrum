"""
SQLAlchemy ORM models for the autism-bias research platform.

These mirror the frontend's lib/types.ts shapes and are designed for
SQLite in development (swap to Postgres by changing DATABASE_URL).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from app.core.db import Base


def _uuid() -> str:
    return str(uuid.uuid4())


# ── Persona ──────────────────────────────────────────────────────────────────

class Persona(Base):
    __tablename__ = "personas"

    id = Column(String, primary_key=True, default=_uuid)
    label = Column(
        String,
        nullable=False,
        comment="non_autistic | autistic_tier_1 | autistic_tier_2 | autistic_tier_3",
    )
    traits = Column(JSON, nullable=False, default=list)

    # Back-references
    conversations_as_a = relationship(
        "Conversation", foreign_keys="Conversation.agent_a_id", back_populates="agent_a"
    )
    conversations_as_b = relationship(
        "Conversation", foreign_keys="Conversation.agent_b_id", back_populates="agent_b"
    )


# ── Conversation ─────────────────────────────────────────────────────────────

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=_uuid)
    scenario = Column(String, nullable=False)
    agent_a_id = Column(String, ForeignKey("personas.id"), nullable=False)
    agent_b_id = Column(String, ForeignKey("personas.id"), nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    agent_a = relationship("Persona", foreign_keys=[agent_a_id], back_populates="conversations_as_a")
    agent_b = relationship("Persona", foreign_keys=[agent_b_id], back_populates="conversations_as_b")
    turns = relationship("ConversationTurn", back_populates="conversation", cascade="all, delete-orphan")
    interview_responses = relationship(
        "InterviewResponse", back_populates="conversation", cascade="all, delete-orphan"
    )
    extracted_features = relationship(
        "ExtractedFeature", back_populates="conversation", cascade="all, delete-orphan"
    )
    classifier_result = relationship(
        "ClassifierResult", back_populates="conversation", uselist=False, cascade="all, delete-orphan"
    )


# ── ConversationTurn ─────────────────────────────────────────────────────────

class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    speaker = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    conversation = relationship("Conversation", back_populates="turns")


# ── InterviewResponse ────────────────────────────────────────────────────────

class InterviewResponse(Base):
    __tablename__ = "interview_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    agent_id = Column(String, ForeignKey("personas.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    conversation = relationship("Conversation", back_populates="interview_responses")
    agent = relationship("Persona")


# ── ExtractedFeature ─────────────────────────────────────────────────────────

class ExtractedFeature(Base):
    __tablename__ = "extracted_features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    feature_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    conversation = relationship("Conversation", back_populates="extracted_features")


# ── ClassifierResult ─────────────────────────────────────────────────────────

class ClassifierResult(Base):
    __tablename__ = "classifier_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(
        String, ForeignKey("conversations.id"), nullable=False, unique=True
    )
    true_label = Column(String, nullable=False)
    predicted_label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)

    conversation = relationship("Conversation", back_populates="classifier_result")


# ── BenchmarkEntry ───────────────────────────────────────────────────────────

class BenchmarkEntry(Base):
    __tablename__ = "benchmark_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String, nullable=False)
    scenario = Column(String, nullable=False)
    dimension = Column(
        String,
        nullable=False,
        comment="e.g. deficit_framing, stereotype_presence, accommodation_asymmetry, agency_framing",
    )
    score = Column(Float, nullable=False)
    justification = Column(Text, nullable=False, default="")
