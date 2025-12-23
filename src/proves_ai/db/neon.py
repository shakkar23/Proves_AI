from __future__ import annotations

from typing import Iterable

import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

from proves_ai.config import Settings


def build_dsn(settings: Settings) -> str:
    if settings.neon_dsn and settings.neon_dsn.get_secret_value().strip():
        return settings.neon_dsn.get_secret_value()

    missing: list[str] = []
    if not settings.neon_host:
        missing.append("PROVES_NEON_HOST")
    if not settings.neon_db:
        missing.append("PROVES_NEON_DB")
    if not settings.neon_user:
        missing.append("PROVES_NEON_USER")
    if not settings.neon_password or not settings.neon_password.get_secret_value().strip():
        missing.append("PROVES_NEON_PASSWORD")

    if missing:
        missing_text = ", ".join(missing)
        raise ValueError(f"Missing Neon settings: {missing_text}")

    password = settings.neon_password.get_secret_value()
    return (
        f"postgresql://{settings.neon_user}:{password}"
        f"@{settings.neon_host}:{settings.neon_port}/{settings.neon_db}"
        f"?sslmode={settings.neon_sslmode}"
    )


def get_connection(settings: Settings) -> psycopg.Connection:
    dsn = build_dsn(settings)
    conn = psycopg.connect(dsn, row_factory=dict_row)
    register_vector(conn)
    return conn


def ensure_pgvector(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.commit()


def execute_statements(conn: psycopg.Connection, statements: Iterable[str]) -> None:
    with conn.cursor() as cur:
        for statement in statements:
            cur.execute(statement)
        conn.commit()
