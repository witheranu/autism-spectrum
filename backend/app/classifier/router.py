from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.db import get_db
from app.models.domain import ClassifierResult, Conversation, ExtractedFeature
from app.classifier.train import train_models
from app.classifier.predict import predict_conversation_persona

router = APIRouter(prefix="/classifier", tags=["classifier"])

@router.post("/train", status_code=status.HTTP_200_OK)
def retrain_classifier(db: Session = Depends(get_db)):
    """Retrain scikit-learn models on all stored conversation features and persist to disk via joblib."""
    try:
        res = train_models(db)
        # Run inference on all conversations to update ClassifierResults in DB
        conversations = db.query(Conversation).all()
        for conv in conversations:
            try:
                predict_conversation_persona(db, conv.id)
            except Exception:
                pass
        return {"status": "success", "training_summary": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classifier training failed: {str(e)}")

@router.get("/results")
def get_classifier_results(db: Session = Depends(get_db)):
    """Return confusion matrix & classification accuracy data matching the frontend's classifier page format."""
    results = (
        db.query(ClassifierResult)
        .options(
            joinedload(ClassifierResult.conversation).joinedload(Conversation.extracted_features)
        )
        .all()
    )

    formatted_results = []
    for res in results:
        feat_dict = {}
        if res.conversation and res.conversation.extracted_features:
            for ef in res.conversation.extracted_features:
                feat_dict[ef.feature_name] = ef.value
        
        if not feat_dict:
            feat_dict = {
                "literal_interpretation": 0.5,
                "direct_communication": 0.6,
                "sensory_mention": 0.2,
                "routine_preference": 0.4
            }

        formatted_results.append({
            "conversationId": res.conversation_id,
            "trueLabel": res.true_label,
            "predictedLabel": res.predicted_label,
            "confidence": res.confidence,
            "features": feat_dict
        })

    # If database has no classifier results yet, run inference on existing conversations or construct baseline responses
    if not formatted_results:
        conversations = db.query(Conversation).all()
        for conv in conversations:
            try:
                c_res = predict_conversation_persona(db, conv.id)
                ext_feats = db.query(ExtractedFeature).filter(ExtractedFeature.conversation_id == conv.id).all()
                feat_dict = {f.feature_name: f.value for f in ext_feats}
                formatted_results.append({
                    "conversationId": conv.id,
                    "trueLabel": c_res.true_label,
                    "predictedLabel": c_res.predicted_label,
                    "confidence": c_res.confidence,
                    "features": feat_dict
                })
            except Exception:
                pass

    return formatted_results
