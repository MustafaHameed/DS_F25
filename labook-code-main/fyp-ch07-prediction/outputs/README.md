# Output Notes

Generated backend artifacts from the Python pipeline are written into `outputs/backend/`.

This folder is intentionally empty before the pipeline runs.

Expected artifacts include:

- model metrics by week
- top feature rankings
- student-level prediction exports
- `dashboard.json` for the web frontend
- trained `.joblib` model files under `outputs/backend/models/`