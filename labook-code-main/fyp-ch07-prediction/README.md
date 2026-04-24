# FYP Ch07: Student Success Prediction Dashboard

This folder packages Chapter 07 as a BSIT-style Final Year Project.

## Project Title

Student Success Prediction Dashboard for Moodle Learning Analytics

## Problem Statement

Universities collect large volumes of Moodle interaction data, but instructors often lack a practical way to transform those logs into early risk alerts. This project builds a prediction pipeline and dashboard that identify students who may struggle in a course using only the first weeks of LMS activity.

## Objectives

1. Build a reproducible Python-based backend for preprocessing Moodle event logs and assessment data.
2. Engineer behavior-based features such as activity counts, session patterns, entropy, and active-day gaps.
3. Train week-by-week Random Forest models for course-outcome classification and final-grade regression.
4. Export dashboard-ready outputs for a web frontend.
5. Provide a notebook equivalent of the original QMD workflow while keeping the runtime free of any R dependency.
6. Present results in a web interface that supports risk review, model monitoring, and feature interpretation.

## Dataset

This FYP uses a local copy of the Chapter 07 dataset:

- `data/raw/Events.xlsx`
- `data/raw/Results.xlsx`

The original source lives in the repository dataset collection, but this project keeps its own copies to remain self-contained.

## Project Structure

```text
fyp-ch07-prediction/
├── backend/
│   └── run_prediction_pipeline.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── docs/
│   └── project-brief.md
├── frontend/
│   ├── css/styles.css
│   ├── js/app.js
│   └── index.html
├── outputs/
│   └── README.md
└── run/
    ├── run_backend.ps1
    ├── run_notebook.ps1
    └── run_frontend.ps1
```

## Source Translation

This FYP is derived from the original Chapter 07 analytical sources:

- Original QMD concept source: `../ch07-prediction/ch07-prediction.qmd`
- Python notebook equivalent: `../ch07-prediction/ch07-prediction.ipynb`

The FYP runtime uses `backend/run_prediction_pipeline.py` so the project can run without R. The original QMD and the existing notebook remain the conceptual and pedagogical reference for the translated backend.

## Backend Workflow

The Python backend does the following:

1. Reads local copies of the Moodle events and results files.
2. Reconstructs course weeks from timestamps.
3. Creates learning sessions using a 1.5-hour inactivity threshold.
4. Builds weekly classification and regression datasets.
5. Trains Random Forest models for weeks 1 through 5.
6. Selects the best classification week by `F1` and the best regression week by `R2`.
7. Exports CSV, JSON, pickle, and model artifacts for the dashboard.

The translated workflow mirrors the original QMD concepts, but it runs entirely through Python.

## Frontend Workflow

The web frontend reads `outputs/backend/dashboard.json` and renders:

- overview KPIs
- weekly model performance charts
- feature-importance charts
- a searchable student risk table

## Run Instructions

### 1. Run backend

From PowerShell:

```powershell
.\run\run_backend.ps1
```

### 2. Run frontend

From PowerShell:

```powershell
.\run\run_frontend.ps1
```

Then open:

```text
http://localhost:8507/frontend/index.html
```

### 3. Open the notebook equivalent

If you want the interactive notebook version of the translated Chapter 07 workflow, run:

```powershell
.\run\run_notebook.ps1
```

## Expected Outputs

The backend generates:

- `outputs/backend/classification_metrics_by_week.csv`
- `outputs/backend/regression_metrics_by_week.csv`
- `outputs/backend/student_predictions.csv`
- `outputs/backend/feature_importance_classification.csv`
- `outputs/backend/feature_importance_regression.csv`
- `outputs/backend/dashboard.json`
- `outputs/backend/models/best_classification_model.joblib`
- `outputs/backend/models/best_regression_model.joblib`

## BSIT FYP Framing

This project can be written up as a full BSIT FYP with:

- educational problem context
- system architecture
- machine-learning methodology translated from the original QMD into Python
- dashboard implementation
- evaluation results
- ethical and privacy considerations for student data