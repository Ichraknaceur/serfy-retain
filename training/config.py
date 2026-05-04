from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


@dataclass(frozen=True)
class TrainingConfig:
    raw_data_path: Path
    interim_data_dir: Path
    processed_data_dir: Path
    artifacts_dir: Path
    random_state: int
    test_size: float
    mlflow_tracking_uri: str | None
    mlflow_experiment_name: str
    dagshub_repo_owner: str | None
    dagshub_repo_name: str | None
    run_name: str


def _optional_env(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return value or None


def get_training_config() -> TrainingConfig:
    raw_data_path = Path(os.getenv("RAW_DATA_PATH", DATA_DIR / "raw" / "churn.csv"))
    interim_data_dir = Path(os.getenv("INTERIM_DATA_DIR", DATA_DIR / "interim"))
    processed_data_dir = Path(os.getenv("PROCESSED_DATA_DIR", DATA_DIR / "processed"))
    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", DATA_DIR / "artifacts"))

    return TrainingConfig(
        raw_data_path=raw_data_path,
        interim_data_dir=interim_data_dir,
        processed_data_dir=processed_data_dir,
        artifacts_dir=artifacts_dir,
        random_state=int(os.getenv("TRAIN_RANDOM_STATE", "42")),
        test_size=float(os.getenv("TRAIN_TEST_SIZE", "0.2")),
        mlflow_tracking_uri=_optional_env("MLFLOW_TRACKING_URI"),
        mlflow_experiment_name=os.getenv("MLFLOW_EXPERIMENT_NAME", "serfy-retain-churn"),
        dagshub_repo_owner=_optional_env("DAGSHUB_REPO_OWNER"),
        dagshub_repo_name=_optional_env("DAGSHUB_REPO_NAME"),
        run_name=os.getenv("MLFLOW_RUN_NAME", "lightgbm-baseline"),
    )


def resolve_mlflow_tracking_uri(config: TrainingConfig) -> str | None:
    if config.mlflow_tracking_uri:
        return config.mlflow_tracking_uri

    if config.dagshub_repo_owner and config.dagshub_repo_name:
        return f"https://dagshub.com/{config.dagshub_repo_owner}/{config.dagshub_repo_name}.mlflow"

    return None
