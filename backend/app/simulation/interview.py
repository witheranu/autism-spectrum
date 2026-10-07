from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.domain import Conversation, InterviewResponse
from app.simulation.llm import LLMProvider, MockLLMProvider

DEFAULT_INTERVIEW_QUESTIONS = [
    "How comfortable did you feel during this interaction?",
    "Did you feel your conversation partner understood your intent?",
    "Were there any moments of friction, ambiguity, or misunderstanding?"
]

def run_post_conversation_interview(
    db: Session,
    conversation_id: str,
    questions: List[str] | None = None,
    llm_provider: LLMProvider | None = None
) -> List[InterviewResponse]:
    """Run post-conversation interview questions for both participating agents in a conversation."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise ValueError(f"Conversation {conversation_id} not found.")

    provider = llm_provider or MockLLMProvider()
    questions_to_ask = questions or DEFAULT_INTERVIEW_QUESTIONS

    # Reconstruct transcript text for interview prompt context
    transcript_text = "\n".join([f"{t.speaker}: {t.text}" for t in (conv.turns or [])])

    created_responses = []

    for agent_id in [conv.agent_a_id, conv.agent_b_id]:
        system_prompt = (
            f"You participated as {agent_id} in the following conversation:\n\n"
            f"{transcript_text}\n\n"
            f"Answer the post-conversation debrief questions in-character as {agent_id}. "
            f"Be concise, honest, and direct."
        )

        for q in questions_to_ask:
            answer = provider.generate_response(
                system_prompt=system_prompt,
                messages=[{"role": "user", "content": q}]
            )

            resp = InterviewResponse(
                conversation_id=conv.id,
                agent_id=agent_id,
                question=q,
                answer=answer
            )
            db.add(resp)
            created_responses.append(resp)

    db.commit()
    return created_responses
