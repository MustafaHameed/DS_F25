# Data Notes

This project stores its own local data copy so it can run independently of the original tutorial folder.

## Raw Files

- `raw/Events.xlsx`: Moodle event-log export used for interaction preprocessing.
- `raw/Results.xlsx`: course results file used for outcome and grade targets.

## Processed Files

The backend generates these after execution:

- `processed/events.csv`
- `processed/events_with_sessions.csv`
- `processed/final_grades.csv`

## Handling Rules

1. Keep the copied raw files unchanged.
2. Regenerate processed files from the backend instead of editing them manually.
3. Do not point this FYP back to the shared `data-main` folder once local copies exist.