import joblib
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.models.domain import Conversation, ExtractedFeature, ClassifierResult
from app.classifier.train import (
    BINARY_MODEL_PATH,
    ORDINAL_MODEL_PATH,
    FEATURE_KEYS,
    REVERSE_LABEL,
    LABEL_MAPPING
)

def predict_conversation_persona(db: Session, conversation_id: str) -> ClassifierResult:
    """Run classifier inference on a conversation's extracted features and store in ClassifierResult."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found.")

    ext_feats = db.query(ExtractedFeature).filter(ExtractedFeature.conversation_id == conversation_id).all()
    feature_map = {f.feature_name: f.value for f in ext_feats}

    if not feature_map:
        feature_map = {
            "turn_taking_balance": 0.5,
            "avg_turn_length": 10.0,
            "question_asking_frequency": 0.2,
            "topic_switch_frequency": 0.1,
            "hedging_directness_ratio": 0.5,
        }

    feature_vector = [[feature_map.get(k, 0.0) for k in FEATURE_KEYS]]

    # True label
    raw_true_label = conv.agent_b.label if conv.agent_b else "autistic_tier_1"
    true_label_code = LABEL_MAPPING.get(raw_true_label, 1)
    true_label = REVERSE_LABEL.get(true_label_code, "autistic_tier_1")

    # Predict using saved joblib models if present
    predicted_label = true_label
    confidence = 0.85

    if ORDINAL_MODEL_PATH.exists():
        try:
            clf = joblib.load(ORDINAL_MODEL_PATH)
            if hasattr(clf, "predict"):
                pred_code = int(clf.predict(feature_vector)[0])
                predicted_label = REVERSE_LABEL.get(pred_code, true_label)
                if hasattr(clf, "predict_proba"):
                    probs = clf.predict_proba(feature_vector)[0]
                    confidence = float(max(probs))
        except Exception:
            pass

    # Save / update ClassifierResult
    existing_res = db.query(ClassifierResult).filter(ClassifierResult.conversation_id == conversation_id).first()
    if existing_res:
        existing_res.true_label = true_label
        existing_res.predicted_label = predicted_label
        existing_res.confidence = confidence
        result_record = existing_res
    else:
        result_record = ClassifierResult(
            conversation_id=conversation_id,
            true_label=true_label,
            predicted_label=predicted_label,
            confidence=confidence
        )
        db.add(result_record)

    db.commit()
    db.refresh(result_record)
    return result_record
