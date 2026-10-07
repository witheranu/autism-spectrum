from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.domain import BenchmarkEntry, Conversation
from app.bias.scoring import score_conversation_bias
from app.simulation.llm import OpenAILLMProvider, MockLLMProvider

router = APIRouter(prefix="/bias", tags=["bias"])

@router.post("/score/{conversation_id}", status_code=status.HTTP_201_CREATED)
def trigger_bias_scoring(
    conversation_id: str,
    use_mock: bool = True,
    model_name: str = "GPT-4o",
    db: Session = Depends(get_db)
):
    """Trigger lexicon + LLM judge bias scoring for a specific conversation."""
    provider = MockLLMProvider() if use_mock else OpenAILLMProvider()
    try:
        entries = score_conversation_bias(
            db=db,
            conversation_id=conversation_id,
            llm_provider=provider,
            model_name=model_name
        )
        return {
            "conversation_id": conversation_id,
            "status": "scored",
            "entries_count": len(entries)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias scoring failed: {str(e)}")

@router.get("/scores")
def get_bias_scores(db: Session = Depends(get_db)):
    """Return benchmark leaderboard results grouped by model and scenario, matching frontend expected JSON format."""
    entries = db.query(BenchmarkEntry).all()

    # Group entries by (model_name, scenario)
    grouped: Dict[tuple, List[BenchmarkEntry]] = {}
    for entry in entries:
        key = (entry.model_name, entry.scenario)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(entry)

    formatted_results = []
    for (model, scenario), dim_entries in grouped.items():
        bias_scores = [
            {
                "dimension": e.dimension,
                "score": e.score,
                "justification": e.justification
            }
            for e in dim_entries
        ]
        
        # Calculate overall score as mean of dimension scores
        avg_score = round(sum(e.score for e in dim_entries) / len(dim_entries), 1) if dim_entries else 0.0

        formatted_results.append({
            "model": model,
            "scenario": scenario,
            "overallScore": avg_score,
            "biasScores": bias_scores
        })

    # Fallback response matching frontend benchmark leaderboard format if DB has no entries yet
    if not formatted_results:
        conversations = db.query(Conversation).all()
        for conv in conversations:
            try:
                entries = score_conversation_bias(db, conv.id, model_name="GPT-4o")
                dim_scores = [
                    {
                        "dimension": e.dimension,
                        "score": e.score,
                        "justification": e.justification
                    }
                    for e in entries
                ]
                avg = round(sum(e.score for e in entries) / len(entries), 1) if entries else 80.0
                formatted_results.append({
                    "model": "GPT-4o",
                    "scenario": conv.scenario,
                    "overallScore": avg,
                    "biasScores": dim_scores
                })
            except Exception:
                pass

    return formatted_results

@router.get("/benchmark")
def get_benchmark_leaderboard(db: Session = Depends(get_db)):
    """Return benchmark leaderboard results matching the frontend's benchmark page shape."""
    return get_bias_scores(db=db)

