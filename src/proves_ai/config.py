from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PROVES_",
        extra="ignore",
    )

    # Neon (Postgres)
    neon_dsn: SecretStr | None = Field(default=None)
    neon_host: str | None = Field(default=None)
    neon_db: str | None = Field(default=None)
    neon_user: str | None = Field(default=None)
    neon_password: SecretStr | None = Field(default=None)
    neon_port: int = Field(default=5432)
    neon_sslmode: str = Field(default="require")

    # pgvector
    pgvector_schema: str = Field(default="public")
    pgvector_table: str = Field(default="embeddings")
    pgvector_dim: int = Field(default=384)

    # Hugging Face
    hf_token: SecretStr | None = Field(default=None)
    hf_cache_dir: str = Field(default=".cache/huggingface")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
    )
    reranker_model: str = Field(
        default="cross-encoder/ms-marco-MiniLM-L-6-v2",
    )


def get_settings() -> Settings:
    return Settings()
