# FYP Ch09: Student Engagement Profile Studio

This folder packages Chapter 09 as a BSIT-style Final Year Project.

## Project Title

Student Engagement Profile Studio using Model-Based Clustering

## Problem Statement

Academic support teams often need to identify hidden engagement profiles among students, but they rarely have an interactive system that turns engagement indicators into interpretable latent groups. This FYP translates the Chapter 09 model-based clustering concepts into a Python-first workflow that discovers engagement profiles and lets a user manually enter a new student pattern to inspect profile probabilities.

## Objectives

1. Align the project with the Chapter 09 QMD concept of latent profile discovery.
2. Use the original Chapter 09 school-engagement dataset rather than the unrelated MOOC centrality dataset.
3. Fit a Python Gaussian Mixture Model that mirrors the chapter's model-based clustering logic.
4. Export profile assignments, posterior probabilities, and profile means for a web dashboard.
5. Provide a manual-input interface where a user can enter engagement values and see profile probabilities.
6. Preserve QMD fidelity while eliminating any R runtime requirement.

## Source Translation

This FYP is derived from:

- Original QMD concept source: `../ch09-model-based-clustering/ch09-model.qmd`
- Python notebook starting point: `../ch09-model-based-clustering/ch09-model-based-clustering.ipynb`

The original notebook diverged from the QMD source by using a different dataset. This packaged FYP corrects that mismatch by using the Chapter 09 engagement dataset and the QMD's three-variable latent-profile framing.

## Dataset

This project uses a local copy of:

- `data/raw/Manuscript_School Engagment.csv`

Selected Chapter 09 features:

- `PRE_ENG_COND` -> `BehvEngmnt`
- `PRE_ENG_COGN` -> `CognEngmnt`
- `PRE_ENG_EMOC` -> `EmotEngmnt`

## Project Structure

```text
fyp-ch09-model-based-clustering/
├── backend/
│   └── run_model_based_pipeline.py
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
│   └── backend/
└── run/
    ├── run_backend.ps1
    ├── run_frontend.ps1
    └── run_notebook.ps1
```

## Backend Workflow

The Python backend does the following:

1. Loads the Chapter 09 engagement dataset from the local FYP copy.
2. Selects the three engagement indicators used by the QMD chapter.
3. Standardizes the features.
4. Fits diagonal-covariance Gaussian Mixture Models for comparison.
5. Preserves a three-profile solution to stay faithful to the chapter framing.
6. Exports assignments, posterior probabilities, profile summaries, and a frontend JSON contract.

## Frontend Workflow

The web frontend renders:

- component selection trends
- profile means and sizes
- manual-input probability scoring for a new student
- a searchable table of assigned students

## Run Instructions

### 1. Run backend

```powershell
.\run\run_backend.ps1
```

### 2. Run frontend

```powershell
.\run\run_frontend.ps1
```

Then open:

```text
http://localhost:8509/frontend/index.html
```

### 3. Open the notebook equivalent

```powershell
.\run\run_notebook.ps1
```

## Expected Outputs

- `outputs/backend/profile_assignments.csv`
- `outputs/backend/profile_means.csv`
- `outputs/backend/model_selection.csv`
- `outputs/backend/dashboard.json`
- `outputs/backend/models/gmm.joblib`
- `outputs/backend/models/scaler.joblib`

## BSIT FYP Framing

This project is suitable as an FYP because it combines:

- educational data mining
- probabilistic machine learning
- interpretable latent-profile analysis
- interactive web-based stakeholder demonstration
