import os
from pathlib import Path
import yaml
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.domain import Conversation, ConversationTurn, Persona
from app.simulation.agent import Agent
from app.simulation.scenarios import get_scenario
from app.simulation.llm import LLMProvider

CONFIGS_DIR = Path(__file__).parent / "persona_configs"

def load_persona_config(persona_id: str) -> dict:
    """Load persona configuration from YAML or create standard fallback."""
    # Map label to filename if needed
    filename = persona_id if persona_id.endswith(".yaml") else f"{persona_id}.yaml"
    file_path = CONFIGS_DIR / filename
    
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
            
    # Default fallback shape
    return {
        "name": persona_id,
        "label": persona_id,
        "traits": ["Default persona traits"],
        "system_prompt": "Participate politely in the conversation."
    }

def get_or_create_persona_record(db: Session, persona_config: dict) -> Persona:
    persona_id = persona_config.get("name", "unknown")
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not db_persona:
        db_persona = Persona(
            id=persona_id,
            label=persona_config.get("label", persona_id),
            traits=persona_config.get("traits", [])
        )
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
    return db_persona

def run_simulation(
    db: Session,
    scenario_id: str,
    agent_a_persona_id: str,
    agent_b_persona_id: str,
    llm_provider: LLMProvider | None = None
) -> Conversation:
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise ValueError(f"Scenario '{scenario_id}' not found.")
        
    config_a = load_persona_config(agent_a_persona_id)
    config_b = load_persona_config(agent_b_persona_id)
    
    persona_a_db = get_or_create_persona_record(db, config_a)
    persona_b_db = get_or_create_persona_record(db, config_b)
    
    agent_a = Agent(persona_config=config_a, provider=llm_provider)
    agent_b = Agent(persona_config=config_b, provider=llm_provider)
    
    # Create DB Conversation Record
    conversation = Conversation(
        scenario=scenario.title,
        agent_a_id=persona_a_db.id,
        agent_b_id=persona_b_db.id,
        created_at=datetime.now(timezone.utc)
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    # Alternating Turn Execution Loop
    turns_count = scenario.num_turns
    current_speaker, current_listener = agent_a, agent_b
    
    # Initial seed prompt to kick off conversation
    current_listener.receive_message("System", f"Let's start discussing: {scenario.context_description}")
    
    for turn_idx in range(turns_count):
        speaker_name = current_speaker.name
        utt_text = current_speaker.speak(scenario.context_description)
        
        # Save turn to DB
        db_turn = ConversationTurn(
            conversation_id=conversation.id,
            speaker=speaker_name,
            text=utt_text,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(db_turn)
        
        # Pass turn utterance to listener agent
        current_listener.receive_message(speaker_name, utt_text)
        
        # Swap turns
        current_speaker, current_listener = current_listener, current_speaker
        
    db.commit()
    db.refresh(conversation)
    return conversation
