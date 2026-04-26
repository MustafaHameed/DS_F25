# FYP Ch11: Longitudinal Engagement Trajectory Studio

## Project Title

Longitudinal Engagement Trajectory Studio for Educational Sequence Modeling

## Problem Statement

Weekly engagement indicators can change over time, so a single static score does not fully describe how students progress. This project translates Chapter 11 into a Python-based FYP that discovers latent engagement states, combines them into learner trajectories, and supports manual trajectory testing through a browser dashboard.

## Core Idea

- Source concept: Chapter 11 VaSSTra workflow from variables to states to trajectories.
- Source data: local copy of `LongitudinalEngagement.csv`.
- Python runtime: course-wise standardization, Gaussian-mixture state discovery, and trajectory clustering.
- Frontend: a web dashboard with manual state-sequence input.

## Run Order

1. Run `./run/run_backend.ps1`
2. Run `./run/run_frontend.ps1`
3. Open `http://127.0.0.1:8511/frontend/index.html`