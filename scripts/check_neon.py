from proves_ai.config import get_settings
from proves_ai.db.neon import ensure_pgvector, get_connection
from proves_ai.retrieval.pgvector import init_vector_table


def main() -> None:
    settings = get_settings()
    with get_connection(settings) as conn:
        ensure_pgvector(conn)
        init_vector_table(conn, settings)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok;")
            row = cur.fetchone()
    print(f"Neon connection ok: {row}")


if __name__ == "__main__":
    main()
