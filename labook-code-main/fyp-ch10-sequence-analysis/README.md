# FYP Ch10: Learning Session Sequence Studio

## Project Title

Learning Session Sequence Studio for Moodle Sequence Analysis

## Problem Statement

Raw Moodle logs show what students clicked, but they do not immediately show the shape of complete learning sessions. This project translates Chapter 10 into a Python-based FYP that sessionizes Moodle events, clusters session traces, and lets a user test a new sequence against the discovered session patterns.

## Core Idea

- Source concept: Chapter 10 sequence analysis and clustering.
- Source data: local copy of `Events.xlsx` from the Moodle course dataset.
- Python runtime: sessionization, sequence-table construction, one-hot sequence encoding, and cluster discovery.
- Frontend: a web dashboard with manual sequence input.

## Folder Guide

- `backend/`: reproducible Python pipeline.
- `data/raw/`: local dataset copy used by the package.
- `data/processed/`: sessionized event outputs.
- `outputs/backend/`: dashboard JSON and CSV artifacts.
- `frontend/`: web-based FYP interface.
- `run/`: launch scripts for backend, frontend, and notebook.

## Run Order

1. Run `./run/run_backend.ps1`
2. Run `./run/run_frontend.ps1`
3. Open `http://127.0.0.1:8510/frontend/index.html`