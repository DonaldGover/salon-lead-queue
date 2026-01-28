"""
Application Configuration
=========================

Loads settings from environment variables.
Never stores secrets in code - all sensitive values come from .env file.
"""
import os
from pathlib import Path
from functools import lru_cache


class Settings:
    """Application settings loaded from environment."""

    def __init__(self):
        # Server
        self.host: str = os.getenv("HOST", "127.0.0.1")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        # Database
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql://localhost:5432/salon_leads"
        )

        # Paths
        self.base_dir: Path = Path(__file__).parent
        self.templates_dir: Path = self.base_dir / "templates"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
