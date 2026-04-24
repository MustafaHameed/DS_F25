# FYP Ch07: Student Success Prediction Dashboard

This folder packages Chapter 07 as a BSIT-style Final Year Project.

## Project Title

Student Success Prediction Dashboard for Moodle Learning Analytics

## Problem Statement

Universities collect large volumes of Moodle interaction data, but instructors often lack a practical way to transform those logs into early risk alerts. This project builds a prediction pipeline and dashboard that identify students who may struggle in a course using only the first weeks of LMS activity.

## Objectives

1. Build a reproducible R-based backend for preprocessing Moodle event logs and assessment data.
2. Engineer behavior-based features such as activity counts, session patterns, entropy, and active-day gaps.
3. Train week-by-week Random Forest models for course-outcome classification and final-grade regression.
4. Export dashboard-ready outputs for a web frontend.
5. Present results in a web interface that supports risk review, model monitoring, and feature interpretation.

## Dataset

This FYP uses a local copy of the Chapter 07 dataset:

- `data/raw/Events.xlsx`
- `data/raw/Results.xlsx`

The original source lives in the repository dataset collection, but this project keeps its own copies to remain self-contained.

## Project Structure

```text
fyp-ch07-prediction/
├── backend/
│   ├── feature_creation.R
│   ├── model_develop_and_eval.R
│   └── run_prediction_pipeline.R
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
    └── run_frontend.ps1
```

## Backend Workflow

The R backend does the following:

1. Reads local copies of the Moodle events and results files.
2. Reconstructs course weeks from timestamps.
3. Creates learning sessions using a 1.5-hour inactivity threshold.
4. Builds weekly classification and regression datasets.
5. Trains Random Forest models for weeks 1 through 5.
6. Selects the best classification week by `F1` and the best regression week by `R2`.
7. Exports CSV and JSON artifacts for the dashboard.

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

## Expected Outputs

The backend generates:

- `outputs/backend/classification_metrics_by_week.csv`
- `outputs/backend/regression_metrics_by_week.csv`
- `outputs/backend/student_predictions.csv`
- `outputs/backend/feature_importance_classification.csv`
- `outputs/backend/feature_importance_regression.csv`
- `outputs/backend/dashboard.json`

## BSIT FYP Framing

This project can be written up as a full BSIT FYP with:

- educational problem context
- system architecture
- machine-learning methodology
- dashboard implementation
- evaluation results
- ethical and privacy considerations for student data