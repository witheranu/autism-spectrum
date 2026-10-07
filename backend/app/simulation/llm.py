import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import dotenv

dotenv.load_dotenv()

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """Generate LLM response given a system prompt and message history."""
        pass


class OpenAILLMProvider(LLMProvider):
    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None

        if self.api_key:
            try:
                import openai
                self._client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                self._client = None

    def generate_response(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        if not self._client or not self.api_key:
            # Fallback mock response when no API key is provided
            last_msg = messages[-1]["content"] if messages else "Hello"
            return f"[Mock OpenAI Response]: I acknowledge your point ('{last_msg[:30]}...'). Let's proceed with our goal."

        formatted_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self._client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""


class MockLLMProvider(LLMProvider):
    def generate_response(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        last_msg = messages[-1]["content"] if messages else "Hello"
        return f"[Simulated Response]: Direct follow-up to: '{last_msg[:40]}'."
