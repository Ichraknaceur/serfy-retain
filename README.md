# Serfy Retain

Serfy Retain is a bank churn prevention product.
The goal is to build a clear, modular, and scalable platform that combines:

- churn risk prediction,
- retention offer recommendations,
- AI-assisted personalization,
- product and data monitoring.

## Why This New Project

The previous folders contain strong building blocks, but also a mix of iterations, paths, tests, and CI/CD logic that makes the project harder to evolve safely.
This repository provides a clean foundation with:

- a readable architecture,
- simple conventions,
- a clear backend entry point,
- a lightweight frontend UI,
- dedicated space for monitoring and data.

## Sprint 0 Documentation

The initial framing documents are available in `docs/`:

- [Sprint 0](docs/SPRINT_0.md)
- [Product Brief](docs/product-brief.md)
- [MVP Scope](docs/mvp-scope.md)
- [Technical Architecture](docs/technical-architecture.md)

## Product Positioning

Product name: `Serfy Retain`

Tagline:
`The retention intelligence layer for retail banking.`

Promise:
`Identify at-risk customers, recommend the right action, and industrialize retention workflows.`

## Current Project Status

The project currently includes:

- a Docker-first workflow,
- a baseline `LightGBM` churn pipeline,
- MLflow experiment tracking,
- DagsHub remote tracking,
- generated local model artifacts,
- a backend that loads trained artifacts,
- `/health`, `/model-info`, and `/predict` API routes.

## Structure

```text
serfy-retain/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── requirements-dev.txt
│   └── requirements.txt
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── artifacts/
├── docs/
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── monitoring/
│   └── README.md
├── tests/
│   └── test_health.py
├── training/
│   ├── config.py
│   ├── data_contract.py
│   ├── evaluate.py
│   ├── preprocess.py
│   ├── train.py
│   ├── Dockerfile
│   └── README.md
├── .env.example
├── .gitignore
├── Makefile
├── requirements-ml.txt
└── docker-compose.yml
```

## Recommended Workflow

This project is Docker-first.
You do not need to install Python, Streamlit, or MLflow locally for the main development flow.

Start by listing the available commands:

```bash
make help
```

## Core Commands

Build all Docker images:

```bash
make build
```

Start backend and frontend:

```bash
make up
```

Start only the backend:

```bash
make run-backend
```

Start only the frontend stack:

```bash
make run-frontend
```

Prepare the dataset:

```bash
make preprocess-data
```

Train the churn baseline:

```bash
make train-model
```

Open the local MLflow UI:

```bash
make mlflow-ui
```

Run the test suite:

```bash
make test
```

## Dataset Location

The training flow expects the churn dataset at:

```text
data/raw/churn.csv
```

If needed, you can override that path with `RAW_DATA_PATH`.

## Docker + MLflow Sequence

Recommended end-to-end sequence:

1. Build the Docker images.
2. Run preprocessing if needed.
3. Train the baseline model.
4. Verify local artifacts.
5. Open MLflow locally.
6. Verify the remote run in DagsHub.

Commands:

```bash
make build
make preprocess-data
make train-model
make mlflow-ui
```

Local MLflow UI:

- [http://localhost:5001](http://localhost:5001)

Remote DagsHub MLflow endpoint:

- [https://dagshub.com/Ichraknaceur/serfy-retain.mlflow](https://dagshub.com/Ichraknaceur/serfy-retain.mlflow)

## Environment Configuration

The local `.env` file contains the DagsHub MLflow configuration.
The only value that must remain personal is the token.

```env
MLFLOW_TRACKING_URI=https://dagshub.com/Ichraknaceur/serfy-retain.mlflow
MLFLOW_EXPERIMENT_NAME=serfy-retain-churn
DAGSHUB_REPO_OWNER=Ichraknaceur
DAGSHUB_REPO_NAME=serfy-retain
MLFLOW_TRACKING_USERNAME=Ichraknaceur
MLFLOW_TRACKING_PASSWORD=YOUR_DAGSHUB_TOKEN
```

## Model Artifacts

Training generates local artifacts in:

```text
data/artifacts/
```

Current artifacts:

- `churn_pipeline.joblib`: full fitted pipeline, including preprocessing and model
- `preprocessor.joblib`: fitted preprocessing transformer
- `churn_model.joblib`: trained LightGBM model
- `feature_names.json`: transformed feature list
- `metadata.json`: model metadata and evaluation metrics

These artifacts allow the backend to serve predictions without retraining the model.

## API Status

The backend is already wired to the generated model artifacts.

Available routes:

- `GET /health`
- `GET /model-info`
- `POST /predict`

Example prediction payload:

```json
{
  "customer_age": 45,
  "gender": "M",
  "dependent_count": 2,
  "education_level": "Graduate",
  "marital_status": "Married",
  "income_category": "$60K - $80K",
  "card_category": "Blue",
  "months_on_book": 36,
  "total_relationship_count": 4,
  "months_inactive_12_mon": 2,
  "contacts_count_12_mon": 3,
  "credit_limit": 10000.0,
  "total_revolving_bal": 1500.0,
  "avg_open_to_buy": 8500.0,
  "total_amt_chng_q4_q1": 1.5,
  "total_trans_amt": 5000.0,
  "total_trans_ct": 50,
  "total_ct_chng_q4_q1": 1.2,
  "avg_utilization_ratio": 0.15
}
```

## Local Artifacts vs MLflow Artifacts

There are two artifact layers in the project:

- local project artifacts stored in `data/artifacts/`
- MLflow artifacts logged during a training run

The local artifacts are the files the backend can load directly.
The MLflow artifacts are attached to tracked experiment runs.

## Next Steps

1. Connect the prediction API to the Streamlit frontend.
2. Add backend tests for artifact loading and prediction.
3. Expose prediction examples in the frontend.
4. Add retention recommendation logic on top of the churn score.
5. Extend monitoring with `Evidently` and CI/CD with `Jenkins`.
