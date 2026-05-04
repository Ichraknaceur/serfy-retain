# Training Foundation

This module contains the Sprint 1 machine learning foundation for `Serfy Retain`.

## Scope

The current training flow covers:

- data contract normalization,
- feature engineering,
- train/validation split,
- `LightGBM` baseline training,
- local artifact persistence,
- `MLflow` tracking,
- remote DagsHub tracking,
- backend-compatible artifact generation.

## Expected Input Dataset

By default, training expects a CSV file at:

```text
data/raw/churn.csv
```

You can override it with `RAW_DATA_PATH` if needed.

## Recommended Commands

This project is intended to run through Docker:

```bash
make preprocess-data
make train-model
make mlflow-ui
```

## Direct Docker Commands

If you want to run the training flow without `make`:

```bash
docker compose build ml
docker compose run --rm ml python -m training.preprocess
docker compose run --rm ml python -m training.train
```

## Outputs

Training writes local artifacts to:

```text
data/artifacts/
```

Generated files:

- `churn_pipeline.joblib`
- `preprocessor.joblib`
- `churn_model.joblib`
- `feature_names.json`
- `metadata.json`

These files are later reloaded by the FastAPI backend for inference.

## MLflow and DagsHub

The training job logs metrics and model information to:

- local MLflow UI on port `5001`
- remote DagsHub MLflow tracking using the `.env` configuration

DagsHub endpoint used by this project:

- [https://dagshub.com/Ichraknaceur/serfy-retain.mlflow](https://dagshub.com/Ichraknaceur/serfy-retain.mlflow)

## Current Status

The training pipeline has already been executed successfully and the generated artifacts are available for backend loading.
