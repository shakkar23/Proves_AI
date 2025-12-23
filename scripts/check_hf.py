from proves_ai.config import get_settings
from proves_ai.hf.client import load_embedding_model, load_reranker


def main() -> None:
    settings = get_settings()
    embedder = load_embedding_model(settings)
    tokenizer, model = load_reranker(settings)

    embedding = embedder.encode(["hazard risk test"])
    rerank_inputs = [("hazard risk", "cascade risk in mission planning")]
    tokens = tokenizer(
        [p[0] for p in rerank_inputs],
        [p[1] for p in rerank_inputs],
        return_tensors="pt",
        padding=True,
        truncation=True,
    )
    scores = model(**tokens).logits.squeeze(-1).detach().cpu().tolist()

    print(f"Embedding shape: {embedding.shape}")
    print(f"Reranker scores: {scores}")


if __name__ == "__main__":
    main()
