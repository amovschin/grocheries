"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All runtime configuration values for the application."""

    database_url: str = "sqlite:////data/grocheries.db"
    admin_token: str = "changeme"

    class Config:
        env_file = ".env"

    @property
    def is_sqlite(self) -> bool:
        """Return True when DATABASE_URL points to a SQLite database."""
        return self.database_url.startswith("sqlite")


settings = Settings()
