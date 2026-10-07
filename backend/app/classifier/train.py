import os
from pathlib import Path
from typing import Dict, Tuple, Any
import joblib
from sqlalchemy.orm import Session

from app.models.domain import Conversation, ExtractedFeature

MODEL_DIR = Path(__file__).parent / "saved_models"
BINARY_MODEL_PATH = MODEL_DIR / "binary_classifier.joblib"
ORDINAL_MODEL_PATH = MODEL_DIR / "ordinal_classifier.joblib"

LABEL_MAPPING = {
    "non_autistic": 0,
    "autistic_tier_1": 1,
    "autistic_tier_2": 2,
    "autistic_tier_3": 3,
    "Autistic (Tier 1 - Requiring Support)": 1,
    "Autistic (Tier 2 - Requiring Substantial Support)": 2,
    "Autistic (Tier 3 - Requiring Very Substantial Support)": 3,
    "Neurotypical / Non-Autistic": 0,
}

REVERSE_LABEL = {
    0: "non_autistic",
    1: "autistic_tier_1",
    2: "autistic_tier_2",
    3: "autistic_tier_3",
}

FEATURE_KEYS = [
    "turn_taking_balance",
    "avg_turn_length",
    "question_asking_frequency",
    "topic_switch_frequency",
    "hedging_directness_ratio",
]

def load_dataset_from_db(db: Session) -> Tuple[list, list, list]:
    """Retrieve features and ground-truth persona labels from stored DB conversations."""
    conversations = db.query(Conversation).all()
    X, y_binary, y_ordinal = [], [], []

    for conv in conversations:
        feats = {f.feature_name: f.value for f in (conv.extracted_features or [])}
        if not feats:
            continue
        
        feature_vec = [feats.get(k, 0.0) for k in FEATURE_KEYS]
        
        # Ground truth label from agent B (or persona label)
        raw_label = conv.agent_b.label if conv.agent_b else "autistic_tier_1"
        label_code = LABEL_MAPPING.get(raw_label, 1)

        X.append(feature_vec)
        y_binary.append(0 if label_code == 0 else 1)
        y_ordinal.append(label_code)

    return X, y_binary, y_ordinal

def train_models(db: Session) -> Dict[str, Any]:
    """Train Scikit-Learn pipelines for binary and ordinal classification."""
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        use_sklearn = True
    except ImportError:
        use_sklearn = False

    X, y_bin, y_ord = load_dataset_from_db(db)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if use_sklearn and len(X) >= 2 and len(set(y_bin)) > 1:
        binary_clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=200))
        binary_clf.fit(X, y_bin)

        ordinal_clf = RandomForestClassifier(n_estimators=10, random_state=42)
        ordinal_clf.fit(X, y_ord)

        joblib.dump(binary_clf, BINARY_MODEL_PATH)
        joblib.dump(ordinal_clf, ORDINAL_MODEL_PATH)

        status = "trained_sklearn"
    else:
        # Save mock / placeholder model indicators when data size is small
        joblib.dump({"type": "heuristic_binary"}, BINARY_MODEL_PATH)
        joblib.dump({"type": "heuristic_ordinal"}, ORDINAL_MODEL_PATH)
        status = "trained_heuristic"

    return {
        "status": status,
        "sample_count": len(X),
        "binary_classes": list(set(y_bin)) if y_bin else [],
        "ordinal_classes": list(set(y_ord)) if y_ord else []
    }
