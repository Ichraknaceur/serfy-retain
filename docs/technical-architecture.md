# Technical Architecture

## Principle

The architecture keeps the existing stack, but with a clearer separation between:

- application,
- models,
- experiment tracking,
- monitoring,
- automation.

## Selected Stack

- `FastAPI` for the business API
- `Streamlit` for demos and simple business-facing usage
- `pandas` / `numpy` for data preparation
- `scikit-learn` / `LightGBM` for the churn model
- `MLflow` for experiment tracking
- `DagsHub` for centralized tracking and collaboration
- `Docker` / `docker-compose` for local execution
- `Jenkins` for CI/CD automation
- `Evidently` for data and model monitoring
- `pytest` for testing

## Logical Architecture

```text
Streamlit UI
    |
    v
FastAPI Backend
    |
    +--> Model artifacts service
    +--> Prediction route
    +--> Model info route
    |
    +--> Local artifacts in data/artifacts/

Training pipeline
    |
    +--> preprocessing
    +--> LightGBM training
    +--> local artifact persistence
    +--> MLflow tracking
    +--> DagsHub remote tracking

Monitoring pipeline
    |
    +--> Evidently reports

Automation
    |
    +--> Jenkins pipeline
```

## Backend Structure

```text
backend/app/
├── api/routes/
│   ├── health.py
│   ├── meta.py
│   ├── model.py
│   └── predict.py
├── core/
│   └── config.py
├── schemas/
│   └── prediction.py
├── services/
│   └── model_loader.py
└── main.py
```

## Data and Training Structure

```text
data/
├── raw/
├── interim/
├── processed/
└── artifacts/

training/
├── config.py
├── data_contract.py
├── evaluate.py
├── preprocess.py
├── train.py
└── Dockerfile
```

## Artifact Flow

The current artifact flow is:

1. the dataset is loaded from `data/raw/churn.csv`
2. preprocessing builds the training-ready dataset
3. training fits the pipeline and logs the run to MLflow
4. local artifacts are written to `data/artifacts/`
5. the FastAPI backend reloads those artifacts for inference

## Design Decisions

### Decision 1

The frontend stays on `Streamlit` to accelerate MVP delivery.

### Decision 2

The backend keeps `FastAPI` to isolate prediction services and make testing easier.

### Decision 3

Experiment tracking goes systematically through `MLflow` and `DagsHub` to avoid falling back into a notebook-only workflow.

### Decision 4

The project is Docker-first so local machine setup stays minimal.

### Decision 5

The backend serves inference from persisted artifacts instead of retraining at runtime.
