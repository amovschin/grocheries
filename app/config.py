"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All runtime configuration values for the application."""

    database_url: str = "sqlite:////data/grocheries.db"

    class Config:
        env_file = ".env"


settings = Settings()
