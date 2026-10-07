from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # Database
    DATABASE_URL: str = "sqlite:///./autism_bias.db"

    # LLM API Keys (placeholders for future simulation work)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Application
    APP_ENV: str = "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance so .env is only read once."""
    return Settings()
