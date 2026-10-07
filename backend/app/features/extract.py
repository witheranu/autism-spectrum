import re
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.domain import Conversation, ExtractedFeature

HEDGING_TERMS = {
    "maybe", "perhaps", "possibly", "probably", "might", "could", "would",
    "somewhat", "kind of", "sort of", "appears", "seems", "I think", "I feel", "I guess"
}

DIRECT_TERMS = {
    "must", "should", "need", "always", "never", "definitely", "exactly",
    "clearly", "strictly", "specify", "require", "directly"
}

def extract_conversation_features(db: Session, conversation_id: str) -> Dict[str, float]:
    """Extract 5 linguistic/behavioral metrics from a conversation's turns and save to DB."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found.")

    turns = conv.turns or []
    if not turns:
        # Default zero features for empty conversation
        features = {
            "turn_taking_balance": 0.5,
            "avg_turn_length": 0.0,
            "question_asking_frequency": 0.0,
            "topic_switch_frequency": 0.0,
            "hedging_directness_ratio": 1.0,
        }
    else:
        # 1. Turn-taking balance (ratio of speaker A turns vs total turns, 0.5 is perfectly balanced)
        speakers = [t.speaker for t in turns]
        first_speaker = speakers[0]
        speaker_a_count = sum(1 for s in speakers if s == first_speaker)
        turn_taking_balance = round(speaker_a_count / len(turns), 2)

        # 2. Average turn length (word count)
        total_words = sum(len(t.text.split()) for t in turns)
        avg_turn_length = round(total_words / len(turns), 2)

        # 3. Question-asking frequency (reciprocity: proportion of turns containing '?')
        question_turns = sum(1 for t in turns if "?" in t.text)
        question_asking_frequency = round(question_turns / len(turns), 2)

        # 4. Topic switch frequency (proxy: presence of transition markers / new keywords)
        topic_switch_markers = ["anyway", "moving on", "also", "besides", "speaking of", "by the way", "next topic"]
        topic_switches = 0
        for t in turns:
            text_lower = t.text.lower()
            if any(marker in text_lower for marker in topic_switch_markers):
                topic_switches += 1
        topic_switch_frequency = round(topic_switches / len(turns), 2)

        # 5. Hedging / directness ratio
        all_text_lower = " ".join([t.text.lower() for t in turns])
        hedging_count = sum(len(re.findall(r'\b' + re.escape(term) + r'\b', all_text_lower)) for term in HEDGING_TERMS)
        directness_count = sum(len(re.findall(r'\b' + re.escape(term) + r'\b', all_text_lower)) for term in DIRECT_TERMS) + 1  # smoothing
        hedging_directness_ratio = round(hedging_count / directness_count, 2)

        features = {
            "turn_taking_balance": turn_taking_balance,
            "avg_turn_length": avg_turn_length,
            "question_asking_frequency": question_asking_frequency,
            "topic_switch_frequency": topic_switch_frequency,
            "hedging_directness_ratio": hedging_directness_ratio,
        }

    # Delete existing extracted features for this conversation to allow re-extraction idempotently
    db.query(ExtractedFeature).filter(ExtractedFeature.conversation_id == conversation_id).delete()

    # Save to ExtractedFeature table
    for feat_name, feat_val in features.items():
        db.add(ExtractedFeature(
            conversation_id=conversation_id,
            feature_name=feat_name,
            value=feat_val
        ))

    db.commit()
    return features
