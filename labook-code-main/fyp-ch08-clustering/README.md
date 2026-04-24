# FYP Ch08: Student Network Clustering Studio

This folder packages Chapter 08 as a BSIT-style Final Year Project.

## Project Title

Student Network Clustering Studio for MOOC Centrality Analysis

## Problem Statement

Instructors and learning analysts often have network indicators such as degree, betweenness, and closeness, but they lack a project-style system that can convert those measurements into interpretable student groups. This FYP translates the Chapter 08 clustering concepts from the original QMD tutorial into a Python-first system that identifies network participation profiles and lets a user manually test a new learner profile against the discovered clusters.

## Objectives

1. Translate the Chapter 08 R/QMD clustering concepts into a Python backend.
2. Standardize and cluster student network centrality features using distance-based hierarchical clustering.
3. Evaluate cluster quality using silhouette and Davies-Bouldin metrics.
4. Export dashboard-ready artifacts for a web frontend.
5. Provide a manual-input interface where a user can enter centrality values and see the closest cluster assignment.
6. Keep the original QMD and notebook as conceptual references while avoiding any R runtime dependency.

## Source Translation

This FYP is derived from:

- Original QMD concept source: `../ch08-clustering/ch08-clustering.qmd`
- Python notebook starting point: `../ch08-clustering/ch08-clustering.ipynb`

The packaged runtime is `backend/run_clustering_pipeline.py`. It uses the original QMD concepts of preprocessing, standardization, dissimilarity-aware clustering, and validation, while adding a manual-input assignment workflow suitable for an FYP demonstration.

## Dataset

This project uses local copies of the Chapter 08 source files:

- `data/raw/Centralities.csv`
- `data/raw/DLT1 Nodes.csv`

## Project Structure

```text
fyp-ch08-clustering/
├── backend/
│   └── run_clustering_pipeline.py
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

1. Loads local copies of the centrality data.
2. Keeps only complete numeric feature rows for clustering.
3. Standardizes the centrality measures.
4. Builds Ward-linkage hierarchical clustering solutions.
5. Selects the best cluster count using validation metrics.
6. Exports cluster assignments, cluster profiles, validation metrics, and a frontend contract in JSON.

## Frontend Workflow

The web frontend reads `outputs/backend/dashboard.json` and renders:

- project overview metrics
- cluster-size and validation charts
- cluster profile comparison
- a manual-input form for assigning a new learner profile to the closest cluster
- a searchable table of clustered students

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
http://localhost:8508/frontend/index.html
```

### 3. Open the notebook equivalent

```powershell
.\run\run_notebook.ps1
```

## Expected Outputs

- `outputs/backend/cluster_assignments.csv`
- `outputs/backend/cluster_profiles.csv`
- `outputs/backend/validation_metrics.csv`
- `outputs/backend/dashboard.json`
- `outputs/backend/models/scaler.joblib`

## BSIT FYP Framing

This project is suitable as an FYP because it combines:

- educational network analytics
- unsupervised machine learning
- interactive user-facing interpretation
- a manual demo flow for stakeholder presentations
