"""Application configuration, sourced entirely from the environment.

Every setting has a sane local-dev default so the app boots with zero
configuration. Production deployments override via environment variables
or a `.env` file (see `.env.example`).
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    # --- App metadata ---
    app_name: str = "Hindsight"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # --- HTTP / CORS ---
    cors_allow_origins: list[str] = ["http://localhost:3000"]
    cors_allow_credentials: bool = True

    # --- Logging ---
    log_level: str = "INFO"
    log_json: bool = True

    # --- Our application database (users, roles, tenants, audit log) ---
    # NOT the Cognee store — this is Hindsight's own metadata DB.
    database_url: str = "sqlite+aiosqlite:///./hindsight.db"
    database_echo: bool = False

    # --- Auth (stub for now, see core/security.py) ---
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- Cognee (self-hosted) ---
    # These map to Cognee's own configuration surface. cognee_service.py is
    # the only module allowed to read these / call into the cognee package.
    cognee_llm_provider: str = "openai"
    cognee_llm_model: str = "gpt-4o-mini"
    cognee_llm_api_key: str | None = Field(default=None)
    cognee_llm_endpoint: str | None = Field(default=None)

    cognee_embedding_provider: str = "openai"
    cognee_embedding_model: str = "text-embedding-3-large"
    cognee_embedding_api_key: str | None = Field(default=None)

    cognee_vector_db_provider: str = "lancedb"
    cognee_graph_db_provider: str = "kuzu"

    # Where Cognee stores its own system/data files when self-hosted.
    cognee_system_root_directory: str = ".cognee_system"
    cognee_data_root_directory: str = ".cognee_data"

    # Default dataset used for incident memory unless a tenant/dataset is specified.
    cognee_default_dataset: str = "hindsight_incidents"


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor — import this, not Settings() directly."""
    return Settings()
