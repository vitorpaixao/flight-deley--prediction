# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flight delay prediction project using the 2015 US DOT "Flight Delays and Cancellations" dataset (~5.8M rows). This is an academic project (POS - postgraduate course, Phase 3: Machine Learning Engineering). The project language is Portuguese (Brazilian).

## Development Setup

- **Python 3.13**, managed with **uv** (see `pyproject.toml` and `uv.lock`)
- Virtual environment: `.venv/`
- Install dependencies: `uv sync`
- Install with dev deps (JupyterLab): `uv sync --group dev`
- Run scripts: `uv run python <script.py>` (scripts assume CWD is project root for `data/` paths)
- Launch Jupyter: `uv run jupyter lab`

## Data

Three CSV files in `data/`:
- `flights.csv` — ~5.8M flight records (2.4 GB in memory). Use `low_memory=False` when reading with pandas.
- `airports.csv` — airport metadata
- `airlines.csv` — airline code lookups

Data dictionary is in `plan/dic_data.md`. Original challenge spec PDF is in `plan/origin/`.

### Key data quirks
- Delay cause columns (`AIR_SYSTEM_DELAY`, `SECURITY_DELAY`, `AIRLINE_DELAY`, `LATE_AIRCRAFT_DELAY`, `WEATHER_DELAY`) are ~82% NaN by design — only populated for delayed flights. Impute with 0, not drop.
- `CANCELLATION_REASON` is ~98.5% NaN (only cancelled flights have a reason).
- `DEPARTURE_DELAY`/`ARRIVAL_DELAY` ~1.5% truly missing — drop these rows for modeling.
- Target variable: `IS_DELAYED = DEPARTURE_DELAY > 15` (binary, ~20% positive — moderate imbalance).

## Architecture

- `src/data_analisys/` — standalone data exploration scripts (each reads CSVs directly)
- `notebooks/eda_flights.ipynb` — main EDA notebook with missing value analysis, feature engineering, and train/test split
- `main.py` — project entry point (placeholder)

### Modeling pipeline (from notebook)
1. **Cleaning**: fill delay-cause NaNs with 0, drop rows with null `DEPARTURE_DELAY`
2. **Feature engineering**: `DEP_HOUR` (from `SCHEDULED_DEPARTURE`), `SEASON`, `IS_WEEKEND`, one-hot encoded `AIRLINE`
3. **Features used**: `MONTH`, `DAY_OF_WEEK`, `DEP_HOUR`, `SEASON`, `IS_WEEKEND`, `DISTANCE`, plus airline dummies
4. **Split**: 80/20 train/test with `np.random.default_rng(42)`

### Planned next steps (from notebook conclusions)
- Classification: Logistic Regression vs Random Forest for `IS_DELAYED`
- Regression: Linear Regression vs Random Forest for `DEPARTURE_DELAY` magnitude
- Unsupervised: K-Means clustering, PCA on delay causes
