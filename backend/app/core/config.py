"""Configuration for the FastAPI backend, loaded from environment/.env."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # noqa: DJ001 - empty defaults are intentional (optional overrides)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Translator & Sentiment Analyser API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # CORS origins are configured via env (comma-separated) - never hardcoded secrets.
    cors_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")

    # Input safety limits.
    max_input_chars: int = 1000

    # Inference settings.
    device: str = "cpu"
    hf_home: str = "./HF_HOME"
    hf_token: str = ""

    # Timeout policy (documented): per-request inference soft limit in seconds.
    inference_timeout_seconds: int = 60

    @field_validator("device")
    @classmethod
    def _lower_device(cls, v: str) -> str:
        return v.strip().lower()

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def has_hf_token(self) -> bool:
        return bool(self.hf_token.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
