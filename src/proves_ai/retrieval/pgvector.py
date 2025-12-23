from __future__ import annotations

from typing import Iterable, Sequence

from pgvector.psycopg import Vector
from psycopg import sql
from psycopg.types.json import Json

from proves_ai.config import Settings


def init_vector_table(conn, settings: Settings) -> None:
    schema = sql.Identifier(settings.pgvector_schema)
    table = sql.Identifier(settings.pgvector_table)

    with conn.cursor() as cur:
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(schema))
        cur.execute(
            sql.SQL(
                "CREATE TABLE IF NOT EXISTS {}.{} ("
                "id TEXT PRIMARY KEY, "
                "content TEXT, "
                "metadata JSONB, "
                "embedding VECTOR({})"
                ");"
            ).format(schema, table, sql.Literal(settings.pgvector_dim))
        )
        cur.execute(
            sql.SQL(
                "CREATE INDEX IF NOT EXISTS {} "
                "ON {}.{} USING ivfflat (embedding vector_cosine_ops)"
            ).format(
                sql.Identifier(f"{settings.pgvector_table}_embedding_idx"),
                schema,
                table,
            )
        )
        conn.commit()


def upsert_embeddings(
    conn,
    settings: Settings,
    rows: Iterable[tuple[str, str, dict | None, Sequence[float]]],
) -> None:
    schema = sql.Identifier(settings.pgvector_schema)
    table = sql.Identifier(settings.pgvector_table)

    with conn.cursor() as cur:
        for record_id, content, metadata, embedding in rows:
            cur.execute(
                sql.SQL(
                    "INSERT INTO {}.{} (id, content, metadata, embedding) "
                    "VALUES (%s, %s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET "
                    "content = EXCLUDED.content, "
                    "metadata = EXCLUDED.metadata, "
                    "embedding = EXCLUDED.embedding"
                ).format(schema, table),
                [record_id, content, Json(metadata), Vector(embedding)],
            )
        conn.commit()


def query_similar(
    conn,
    settings: Settings,
    embedding: Sequence[float],
    top_k: int = 5,
) -> list[dict]:
    schema = sql.Identifier(settings.pgvector_schema)
    table = sql.Identifier(settings.pgvector_table)

    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                "SELECT id, content, metadata, "
                "1 - (embedding <=> %s) AS score "
                "FROM {}.{} "
                "ORDER BY embedding <=> %s "
                "LIMIT %s"
            ).format(schema, table),
            [Vector(embedding), Vector(embedding), top_k],
        )
        return list(cur.fetchall())
