from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.pipeline import Pipeline

from training.config import get_training_config, resolve_mlflow_tracking_uri
from training.data_contract import CATEGORICAL_FEATURES, ENGINEERED_FEATURES, MODEL_FEATURES, NUMERICAL_FEATURES
from training.evaluate import evaluate_binary_classification
from training.preprocess import (
    build_preprocessor,
    create_train_validation_split,
    prepare_training_frame,
    split_features_target,
)


def load_prepared_splits(raw_data_path: Path, test_size: float, random_state: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not raw_data_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {raw_data_path}. "
            "Place the CSV file there or override it with RAW_DATA_PATH/--input."
        )

    raw_df = pd.read_csv(raw_data_path)
    prepared_df = prepare_training_frame(raw_df, require_target=True)
    return create_train_validation_split(prepared_df, test_size=test_size, random_state=random_state)


def build_training_pipeline(random_state: int) -> Pipeline:
    model = LGBMClassifier(
        objective="binary",
        random_state=random_state,
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.9,
        colsample_bytree=0.9,
        class_weight="balanced",
        verbosity=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", model),
        ]
    )


def persist_local_artifacts(pipeline: Pipeline, metrics: dict[str, float], artifacts_dir: Path) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    fitted_preprocessor = pipeline.named_steps["preprocessor"]
    fitted_model = pipeline.named_steps["model"]
    feature_names = fitted_preprocessor.get_feature_names_out().tolist()

    joblib.dump(pipeline, artifacts_dir / "churn_pipeline.joblib")
    joblib.dump(fitted_preprocessor, artifacts_dir / "preprocessor.joblib")
    joblib.dump(fitted_model, artifacts_dir / "churn_model.joblib")

    metadata = {
        "model_name": "lightgbm_baseline",
        "target": "target",
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "engineered_features": ENGINEERED_FEATURES,
        "model_features": MODEL_FEATURES,
        "transformed_feature_count": len(feature_names),
        "metrics": metrics,
    }

    with open(artifacts_dir / "feature_names.json", "w", encoding="utf-8") as file:
        json.dump(feature_names, file, indent=2)

    with open(artifacts_dir / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)


def main() -> None:
    config = get_training_config()
    parser = argparse.ArgumentParser(description="Train the Serfy Retain churn baseline.")
    parser.add_argument("--input", type=Path, default=config.raw_data_path)
    parser.add_argument("--artifacts-dir", type=Path, default=config.artifacts_dir)
    args = parser.parse_args()

    tracking_uri = resolve_mlflow_tracking_uri(config)
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    mlflow.set_experiment(config.mlflow_experiment_name)

    train_df, valid_df = load_prepared_splits(
        raw_data_path=args.input,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    X_train, y_train = split_features_target(train_df)
    X_valid, y_valid = split_features_target(valid_df)

    pipeline = build_training_pipeline(config.random_state)

    with mlflow.start_run(run_name=config.run_name):
        pipeline.fit(X_train, y_train)

        y_valid_pred = pipeline.predict(X_valid)
        y_valid_score = pipeline.predict_proba(X_valid)[:, 1]

        metrics = evaluate_binary_classification(y_valid.to_numpy(), y_valid_pred, y_valid_score)

        mlflow.log_params(
            {
                "model_type": "LightGBMClassifier",
                "random_state": config.random_state,
                "test_size": config.test_size,
                "train_rows": len(train_df),
                "validation_rows": len(valid_df),
                "feature_count": len(MODEL_FEATURES),
            }
        )
        mlflow.log_metrics(metrics)
        mlflow.set_tags(
            {
                "product": "Serfy Retain",
                "stack": "python-fastapi-streamlit-lightgbm-mlflow",
                "pipeline_stage": "training",
            }
        )
        mlflow.sklearn.log_model(pipeline, artifact_path="model")

        persist_local_artifacts(pipeline, metrics, args.artifacts_dir)
        mlflow.log_artifacts(str(args.artifacts_dir), artifact_path="local_artifacts")

        print("Training completed successfully.")
        for key, value in metrics.items():
            print(f"{key}: {value:.4f}")
        print(f"Artifacts directory: {args.artifacts_dir}")
        if tracking_uri:
            print(f"MLflow tracking URI: {tracking_uri}")


if __name__ == "__main__":
    main()
