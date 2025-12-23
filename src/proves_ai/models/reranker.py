from __future__ import annotations

from typing import Iterable

import torch


def rerank_pairs(
    tokenizer,
    model,
    pairs: Iterable[tuple[str, str]],
    batch_size: int = 16,
) -> list[float]:
    model.eval()
    scores: list[float] = []

    batch: list[tuple[str, str]] = []
    for pair in pairs:
        batch.append(pair)
        if len(batch) == batch_size:
            scores.extend(_score_batch(tokenizer, model, batch))
            batch = []

    if batch:
        scores.extend(_score_batch(tokenizer, model, batch))

    return scores


def _score_batch(tokenizer, model, batch: list[tuple[str, str]]) -> list[float]:
    inputs = tokenizer(
        [p[0] for p in batch],
        [p[1] for p in batch],
        padding=True,
        truncation=True,
        return_tensors="pt",
    )
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.squeeze(-1)
    return logits.detach().cpu().tolist()
