from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.core.db import get_db
from app.models.domain import Conversation, Persona
from app.simulation.runner import run_simulation
from app.simulation.llm import OpenAILLMProvider, MockLLMProvider

router = APIRouter(tags=["simulation"])

class SimulateRequest(BaseModel):
    scenario_id: str
    agent_a_persona_id: str
    agent_b_persona_id: str
    use_mock: bool = True  # Default to mock provider for fast local execution without mandatory API key

def format_persona_response(persona: Persona) -> dict:
    if not persona:
        return {"id": "unknown", "label": "non_autistic", "traits": []}
    return {
        "id": persona.id,
        "label": persona.label,
        "traits": persona.traits or []
    }

def format_conversation_response(conv: Conversation) -> dict:
    return {
        "id": conv.id,
        "scenario": conv.scenario,
        "agentA": format_persona_response(conv.agent_a),
        "agentB": format_persona_response(conv.agent_b),
        "turns": [
            {
                "speaker": turn.speaker,
                "text": turn.text,
                "timestamp": turn.timestamp.isoformat() if turn.timestamp else ""
            }
            for turn in (conv.turns or [])
        ],
        "interview": [
            {
                "question": resp.question,
                "answer": resp.answer
            }
            for resp in (conv.interview_responses or [])
        ]
    }

@router.post("/simulate", status_code=status.HTTP_201_CREATED)
def trigger_simulation(req: SimulateRequest, db: Session = Depends(get_db)):
    """Trigger a multi-agent conversation simulation run and return the created conversation ID."""
    provider = MockLLMProvider() if req.use_mock else OpenAILLMProvider()
    try:
        conversation = run_simulation(
            db=db,
            scenario_id=req.scenario_id,
            agent_a_persona_id=req.agent_a_persona_id,
            agent_b_persona_id=req.agent_b_persona_id,
            llm_provider=provider
        )
        return {"conversation_id": conversation.id, "status": "completed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation execution failed: {str(e)}")

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    """List all stored conversations formatted for the frontend."""
    conversations = (
        db.query(Conversation)
        .options(
            joinedload(Conversation.agent_a),
            joinedload(Conversation.agent_b),
            joinedload(Conversation.turns),
            joinedload(Conversation.interview_responses)
        )
        .all()
    )
    return [format_conversation_response(c) for c in conversations]

@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get single conversation by ID formatted for frontend consumption."""
    conv = (
        db.query(Conversation)
        .options(
            joinedload(Conversation.agent_a),
            joinedload(Conversation.agent_b),
            joinedload(Conversation.turns),
            joinedload(Conversation.interview_responses)
        )
        .filter(Conversation.id == conversation_id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return format_conversation_response(conv)

@router.post("/conversations/{conversation_id}/interview", status_code=status.HTTP_201_CREATED)
def trigger_interview(conversation_id: str, db: Session = Depends(get_db)):
    """Trigger post-conversation interview debrief questions for agents."""
    from app.simulation.interview import run_post_conversation_interview
    try:
        responses = run_post_conversation_interview(db, conversation_id)
        return {
            "conversation_id": conversation_id,
            "status": "completed",
            "responses_count": len(responses)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interview execution failed: {str(e)}")

