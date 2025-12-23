CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS public.embeddings (
    id TEXT PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(384)
);

CREATE INDEX IF NOT EXISTS embeddings_embedding_idx
    ON public.embeddings USING ivfflat (embedding vector_cosine_ops);
