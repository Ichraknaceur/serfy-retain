from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Serfy Retain API"
    app_env: str = "development"
    app_version: str = "0.1.0"
    frontend_url: str = "http://localhost:8501"
    allowed_origins: str = "http://localhost:8501,http://127.0.0.1:8501"
    artifacts_dir: str = "data/artifacts"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    def resolved_artifacts_dir(self) -> Path:
        path = Path(self.artifacts_dir)
        if path.is_absolute():
            return path

        project_root = Path(__file__).resolve().parents[2]
        return project_root / path


@lru_cache
def get_settings() -> Settings:
    return Settings()
