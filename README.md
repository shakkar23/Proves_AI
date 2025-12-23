# Proves_AI

Repository scaffold for the Proves_AI stack:
- GraphSAGE GNN (PyTorch Geometric) for cascade + graph risk
- XGBoost for mission success probability baseline
- Cross-encoder reranker (Transformers + PEFT/LoRA if needed)
- Embeddings + pgvector in Neon for retrieval

## Quick start
1) Create a virtual environment
2) Install base deps
   - `pip install -r requirements.txt`
3) Install ML deps (GPU/CPU specific)
   - `pip install -r requirements-ml.txt`
   - For PyTorch Geometric, follow the install matrix at https://pytorch-geometric.readthedocs.io
4) Run checks (requires ML deps for Hugging Face)
   - `python scripts/check_neon.py`
   - `python scripts/check_hf.py`

## Environment
Copy `.env.example` to `.env` and fill in values:
- `PROVES_NEON_DSN` or the individual Neon fields
- `PROVES_HF_TOKEN` for Hugging Face access

## Connectivity checks
- Neon: `python scripts/check_neon.py`
- Hugging Face: `python scripts/check_hf.py`

## Repo layout
- `src/proves_ai/config.py`: settings for Neon + HF
- `src/proves_ai/db/neon.py`: Neon connection helpers
- `src/proves_ai/retrieval/pgvector.py`: pgvector schema helpers
- `src/proves_ai/hf/client.py`: HF model loaders
- `src/proves_ai/models/graphsage.py`: GraphSAGE skeleton
- `src/proves_ai/models/xgboost_baseline.py`: XGBoost baseline skeleton
- `src/proves_ai/models/reranker.py`: Cross-encoder loader

## Notes
- This repo is a scaffold; add data loaders and training pipelines under `src/proves_ai/pipelines`.
- Keep secrets in `.env` and out of source control.
- If you prefer SQL setup, run `scripts/init_pgvector.sql` in Neon.
