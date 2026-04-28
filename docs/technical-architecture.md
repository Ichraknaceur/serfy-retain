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
    +--> Prediction service
    +--> Recommendation service
    +--> Model loader
    |
    +--> Model artifacts
    +--> Preprocessor artifacts

Training pipeline
    |
    +--> MLflow tracking
    +--> DagsHub remote tracking

Monitoring pipeline
    |
    +--> Evidently reports

Automation
    |
    +--> Jenkins pipeline
```

## Target Backend Structure

```text
backend/app/
├── api/routes/
├── core/
├── schemas/
├── services/
│   ├── prediction.py
│   ├── recommendation.py
│   └── model_registry.py
└── main.py
```

## Target Data/ML Structure

```text
data/
├── raw/
├── interim/
├── processed/
└── artifacts/

training/
├── preprocess.py
├── train.py
└── evaluate.py
```

## Design Decisions

### Decision 1

The frontend stays on `Streamlit` to accelerate MVP delivery.

### Decision 2

The backend keeps `FastAPI` to isolate prediction and recommendation services and make testing easier.

### Decision 3

Experiment tracking goes systematically through `MLflow` and `DagsHub` to avoid falling back into a notebook-only workflow.

### Decision 4

The AI layer remains optional at the start so it does not delay the MVP's business value.
