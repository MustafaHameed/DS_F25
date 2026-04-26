# FYP Portfolio

This document tracks the Final Year Project packaging work built from Chapters 07 to 21.

The portfolio runtime direction is now Python-first:

- Original `.qmd` files remain the conceptual source of truth.
- Every chapter from `07` to `21` has a verified Python notebook equivalent in the repository.
- FYP packages should run from Python scripts or Jupyter notebooks and must not require R at runtime.
- If a notebook drifts from the QMD chapter, the packaged Python backend should correct that drift.

## Live Projects

### Chapter 07

- Folder: `fyp-ch07-prediction`
- Theme: student success prediction from Moodle activity logs
- Backend: Python feature engineering and Random Forest models
- Notebook equivalent: `ch07-prediction/ch07-prediction.ipynb`
- Frontend: web dashboard
- Status: implemented

### Chapter 08

- Folder: `fyp-ch08-clustering`
- Theme: student network clustering from MOOC centrality measures
- Backend: Python hierarchical clustering with local copied Chapter 08 data
- Notebook equivalent: `ch08-clustering/ch08-clustering.ipynb`
- Frontend: web dashboard with manual centrality input for live cluster assignment
- Status: implemented

### Chapter 09

- Folder: `fyp-ch09-model-based-clustering`
- Theme: latent student engagement profiling from the Chapter 09 school-engagement dataset
- Backend: Python Gaussian Mixture model aligned to the QMD's three-profile framing
- Notebook equivalent: `ch09-model-based-clustering/ch09-model-based-clustering.ipynb`
- Frontend: web dashboard with manual engagement input for live profile probability estimation
- Status: implemented

### Chapter 10

- Folder: `fyp-ch10-sequence-analysis`
- Theme: Moodle session sequence clustering from Chapter 10 event traces
- Backend: Python sessionization, sequence encoding, and cluster discovery using the local copied `Events.xlsx`
- Notebook equivalent: `ch10-sequence-analysis/ch10-sequence-analysis.ipynb`
- Frontend: web dashboard with manual comma-separated sequence input for live cluster assignment
- Status: implemented

### Chapter 11

- Folder: `fyp-ch11-vasstra`
- Theme: longitudinal engagement trajectories from Chapter 11 VaSSTra logic
- Backend: Python course-wise standardization, Gaussian-mixture state discovery, and trajectory clustering
- Notebook equivalent: `ch11-vasstra/ch11-vasstra.ipynb`
- Frontend: web dashboard with eight-step manual state-sequence input
- Status: implemented

### Chapter 12

- Folder: `fyp-ch12-markov-roles`
- Theme: learner role transitions and sequence clusters from Chapter 12 Markov analysis
- Backend: Python observed-transition modeling plus role-sequence mixture clustering on `simulated_roles.csv`
- Notebook equivalent: `ch12-markov/ch12-markov.ipynb`
- Frontend: web dashboard with manual 20-step role-path input
- Status: implemented

### Chapter 13

- Folder: `fyp-ch13-multichannel`
- Theme: multichannel engagement-achievement trajectories from Chapter 13
- Backend: Python paired-sequence encoding and six-cluster multichannel trajectory discovery using the local workbook copy
- Notebook equivalent: `ch13-multichannel/ch13-multichannel.ipynb`
- Frontend: web dashboard with manual paired engagement and achievement input for all eight sequence steps
- Status: implemented

### Chapter 14

- Folder: `fyp-ch14-process-mining`
- Theme: process mining and achiever-group path comparison from Chapter 14
- Backend: Python event-log sessionization, trimmed process-flow extraction, and high/low achiever path scoring
- Notebook equivalent: `ch14-process-mining/ch14-process-mining.ipynb`
- Frontend: web dashboard with manual action-path input scored against group-specific process models
- Status: implemented

## Verified Python Coverage

### Wave A Status

- `ch07-prediction/ch07-prediction.qmd` -> `ch07-prediction/ch07-prediction.ipynb`
- `ch08-clustering/ch08-clustering.qmd` -> `ch08-clustering/ch08-clustering.ipynb`
- `ch09-model-based-clustering/ch09-model.qmd` -> `ch09-model-based-clustering/ch09-model-based-clustering.ipynb`

### Wave B Queue

- `ch10-sequence-analysis/ch10-seq.qmd` -> `ch10-sequence-analysis/ch10-sequence-analysis.ipynb`
- `ch11-vasstra/ch11-vasstra.qmd` -> `ch11-vasstra/ch11-vasstra.ipynb`
- `ch12-markov/ch12-markov.qmd` -> `ch12-markov/ch12-markov.ipynb`
- `ch13-multichannel/ch13-multi.qmd` -> `ch13-multichannel/ch13-multichannel.ipynb`
- `ch14-process-mining/ch14-process.qmd` -> `ch14-process-mining/ch14-process-mining.ipynb`

### Wave C Queue

- `ch15-sna/ch15-sna.qmd` -> `ch15-sna/ch15-sna.ipynb`
- `ch16-community/ch16-comm.qmd` -> `ch16-community/ch16-community.ipynb`
- `ch17-temporal-networks/ch17-tna.qmd` -> `ch17-temporal-networks/ch17-temporal-networks.ipynb`
- `ch18-ena-ona/ch18-ena-ona.qmd` -> `ch18-ena-ona/ch18-ena-ona.ipynb`
- `ch19-psychological-networks/ch19-psych.qmd` -> `ch19-psychological-networks/ch19-psychological-networks.ipynb`

### Wave D Queue

- `ch20-factor-analysis/ch20-fa.qmd` -> `ch20-factor-analysis/ch20-factor-analysis.ipynb`
- `ch21-sem/ch21-sem.qmd` -> `ch21-sem/ch21-sem.ipynb`

## Packaging Notes

### Wave A

- `fyp-ch07-prediction`, `fyp-ch08-clustering`, and `fyp-ch09-model-based-clustering` are now packaged.
- Chapter 07 now includes a browser-side manual prediction demo backed by exported Python model coefficients.
- Chapter 08 uses the existing notebook as a backend starting point and adds a manual-input assignment flow.
- Chapter 09 corrects notebook/QMD drift by using the original engagement dataset and QMD-aligned variables inside the packaged Python backend.

### Wave B

- `fyp-ch10-sequence-analysis`, `fyp-ch11-vasstra`, `fyp-ch12-markov-roles`, `fyp-ch13-multichannel`, and `fyp-ch14-process-mining` are now packaged and validated.
- Chapter 10 corrects notebook drift by using the real `Events.xlsx` session traces and adds a manual session-cluster demo.
- Chapter 11 follows the QMD variables-to-states-to-trajectories flow and adds an eight-step manual state-sequence demo.
- Chapter 12 uses the real role dataset and exposes a manual 20-step role-path classifier.
- Chapter 13 uses the real multichannel workbook, not the drifting synthetic notebook data, and adds paired manual state input.
- Chapter 14 uses the real Moodle event log plus achiever labels and adds a manual action-path scorer.

### Wave C

- `fyp-ch15-sna`
- `fyp-ch16-community`
- `fyp-ch17-temporal-networks`
- `fyp-ch18-ena-ona`
- `fyp-ch19-psychological-networks`

### Wave D

- `fyp-ch20-factor-analysis`
- `fyp-ch21-sem`

## Conventions

Each FYP package should include:

1. Local dataset copies under `data/raw`.
2. A Python backend under `backend/` and, when useful, a linked or copied Jupyter notebook equivalent.
3. A frontend under `frontend` that accepts manual input to demonstrate the project's core use case.
4. Outputs under `outputs`.
5. FYP-oriented documentation under `README.md` and `docs/`.
6. Clear mapping back to the original chapter `.qmd` source.
7. QMD-faithful Python logic when a notebook needs improvement or correction.

## Next Target

The next implementation wave should focus on Chapters 15 to 19, keeping the same Python-first rule, QMD-concept fidelity, local dataset copies, and manual-input frontend requirement.
