"""
Configuration module — loads settings from .env
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-haiku-20240307"

    # SEC EDGAR
    sec_user_agent: str = "AgenticInsiderTrader dev@example.com"

    # Feature Flags
    use_mock_data: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"


settings = Settings()
