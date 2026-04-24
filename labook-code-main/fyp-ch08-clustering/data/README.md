# Data Notes

This project stores its own local data copy so the FYP can run independently.

## Raw Files

- `raw/Centralities.csv`: node-level network centrality measures used for clustering.
- `raw/DLT1 Nodes.csv`: optional supporting node attributes copied for provenance and future extensions.

## Processed Files

The backend generates cleaned clustering-ready files under `processed/`.

## Handling Rules

1. Keep the raw files unchanged.
2. Recreate processed files through the Python backend.
3. Treat the original chapter notebook and QMD as conceptual references, not runtime dependencies.
