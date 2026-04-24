# FYP Portfolio

This document tracks the Final Year Project packaging work built from Chapters 07 to 21.

The portfolio runtime direction is now Python-first:

- Original `.qmd` files remain the conceptual source of truth.
- Every chapter from `07` to `21` has a verified Python notebook equivalent in the repository.
- FYP packages should run from Python scripts or Jupyter notebooks and must not require R at runtime.

## Live Project

### Chapter 07

- Folder: `fyp-ch07-prediction`
- Theme: student success prediction from Moodle activity logs
- Backend: Python feature engineering and Random Forest models
- Notebook equivalent: `ch07-prediction/ch07-prediction.ipynb`
- Frontend: web dashboard
- Status: implemented

## Verified Python Coverage

### Wave A

- `ch07-prediction/ch07-prediction.qmd` -> `ch07-prediction/ch07-prediction.ipynb`
- `ch08-clustering/ch08-clustering.qmd` -> `ch08-clustering/ch08-clustering.ipynb`
- `ch09-model-based-clustering/ch09-model.qmd` -> `ch09-model-based-clustering/ch09-model-based-clustering.ipynb`

### Wave B

- `ch10-sequence-analysis/ch10-seq.qmd` -> `ch10-sequence-analysis/ch10-sequence-analysis.ipynb`
- `ch11-vasstra/ch11-vasstra.qmd` -> `ch11-vasstra/ch11-vasstra.ipynb`
- `ch12-markov/ch12-markov.qmd` -> `ch12-markov/ch12-markov.ipynb`
- `ch13-multichannel/ch13-multi.qmd` -> `ch13-multichannel/ch13-multichannel.ipynb`
- `ch14-process-mining/ch14-process.qmd` -> `ch14-process-mining/ch14-process-mining.ipynb`

### Wave C

- `ch15-sna/ch15-sna.qmd` -> `ch15-sna/ch15-sna.ipynb`
- `ch16-community/ch16-comm.qmd` -> `ch16-community/ch16-community.ipynb`
- `ch17-temporal-networks/ch17-tna.qmd` -> `ch17-temporal-networks/ch17-temporal-networks.ipynb`
- `ch18-ena-ona/ch18-ena-ona.qmd` -> `ch18-ena-ona/ch18-ena-ona.ipynb`
- `ch19-psychological-networks/ch19-psych.qmd` -> `ch19-psychological-networks/ch19-psychological-networks.ipynb`

### Wave D

- `ch20-factor-analysis/ch20-fa.qmd` -> `ch20-factor-analysis/ch20-factor-analysis.ipynb`
- `ch21-sem/ch21-sem.qmd` -> `ch21-sem/ch21-sem.ipynb`

## Packaging Plan

### Wave A

- `fyp-ch08-clustering` should use `ch08-clustering/ch08-clustering.ipynb` as the Python backend starting point.
- `fyp-ch09-model-based-clustering` should use `ch09-model-based-clustering/ch09-model-based-clustering.ipynb` as the Python backend starting point.

### Wave B

- `fyp-ch10-sequence-analysis`
- `fyp-ch11-vasstra`
- `fyp-ch12-markov`
- `fyp-ch13-multichannel`
- `fyp-ch14-process-mining`

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
3. A frontend under `frontend`.
4. Outputs under `outputs`.
5. FYP-oriented documentation under `README.md` and `docs/`.
6. Clear mapping back to the original chapter `.qmd` source.

## Next Target

The next implementation wave should focus on Chapters 08 and 09 so the clustering group is packaged as Python-first FYPs using the existing notebook translations instead of any R runtime.