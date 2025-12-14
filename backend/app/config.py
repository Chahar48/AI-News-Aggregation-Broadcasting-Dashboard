from functools import lru_cache
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """
    Global application configuration for the
    AI News Aggregation & Broadcasting Dashboard (MVP).

    Focused, production-safe, Groq-first config.
    """

    # --------------------
    # App Metadata
    # --------------------
    APP_NAME: str = "AI News Aggregation & Broadcasting Dashboard"
    APP_ENV: str = Field(default="development", env="APP_ENV")

    # --------------------
    # Database
    # --------------------
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # --------------------
    # Groq LLM (MANDATORY)
    # --------------------
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")

    # --------------------
    # Email Broadcast (Mock / Optional)
    # --------------------
    SENDGRID_API_KEY: str | None = Field(default=None, env="SENDGRID_API_KEY")
    EMAIL_FROM: str = Field(default="no-reply@example.com", env="EMAIL_FROM")

    # --------------------
    # LinkedIn (Simulation)
    # --------------------
    LINKEDIN_CLIENT_ID: str | None = Field(default=None, env="LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: str | None = Field(default=None, env="LINKEDIN_CLIENT_SECRET")

    # --------------------
    # Logging
    # --------------------
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # ignore unused env vars safely


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Ensures env vars are read once per process.
    """
    return Settings()
