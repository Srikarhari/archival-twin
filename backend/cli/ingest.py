"""Archive ingestion CLI: scan images, detect faces, extract embeddings, store in SQLite."""
# TODO: CLI entry point — python -m cli.ingest --archive-dir PATH --collection NAME --db PATH
# TODO: Flags: --force, --dry-run, --batch-size N, --metadata-csv PATH
# TODO: V1 — minimal seed script to populate DB for testing
# TODO: V2 — full pipeline with hash-based incremental ingestion, tqdm, collection adapters
