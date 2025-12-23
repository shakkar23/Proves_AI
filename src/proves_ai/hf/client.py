from __future__ import annotations

from pathlib import Path

from proves_ai.config import Settings


def _hf_kwargs(settings: Settings) -> dict:
    kwargs: dict = {"cache_dir": str(Path(settings.hf_cache_dir))}
    if settings.hf_token and settings.hf_token.get_secret_value().strip():
        kwargs["token"] = settings.hf_token.get_secret_value()
    return kwargs


def load_embedding_model(settings: Settings):
    from sentence_transformers import SentenceTransformer

    kwargs = _hf_kwargs(settings)
    return SentenceTransformer(settings.embedding_model, **kwargs)


def load_reranker(settings: Settings):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    kwargs = _hf_kwargs(settings)
    tokenizer = AutoTokenizer.from_pretrained(settings.reranker_model, **kwargs)
    model = AutoModelForSequenceClassification.from_pretrained(
        settings.reranker_model,
        **kwargs,
    )
    return tokenizer, model
