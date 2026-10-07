from typing import List, Dict, Any
from app.simulation.llm import LLMProvider, OpenAILLMProvider

class Agent:
    def __init__(self, persona_config: Dict[str, Any], provider: LLMProvider | None = None):
        self.name: str = persona_config.get("name", "agent")
        self.label: str = persona_config.get("label", "non_autistic")
        self.traits: List[str] = persona_config.get("traits", [])
        self.system_prompt: str = persona_config.get("system_prompt", "")
        self.provider: LLMProvider = provider or OpenAILLMProvider()
        
        # Conversational memory history: [{"role": "user"|"assistant", "content": str}]
        self.memory: List[Dict[str, str]] = []

    def receive_message(self, speaker_name: str, text: str):
        """Append an incoming utterance from another agent into local memory."""
        self.memory.append({"role": "user", "content": f"[{speaker_name}]: {text}"})

    def speak(self, context_description: str) -> str:
        """Generate response based on persona system prompt, task context, and current memory."""
        full_system_prompt = (
            f"{self.system_prompt}\n\n"
            f"Scenario Context: {context_description}\n"
            f"Stay strictly in character. Respond concisely as persona {self.name} ({self.label})."
        )
        
        response_text = self.provider.generate_response(
            system_prompt=full_system_prompt,
            messages=self.memory
        )
        
        # Append own response to local memory as assistant
        self.memory.append({"role": "assistant", "content": response_text})
        return response_text
