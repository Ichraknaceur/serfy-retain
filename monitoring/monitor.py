import json
from pathlib import Path

import joblib
import pandas as pd
from evidently import ColumnMapping
from evidently.metric_preset import ClassificationPreset, DataDriftPreset
from evidently.report import Report

ARTIFACTS_DIR = Path("data/artifacts")
PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("monitoring/reports")


def load_metadata() -> dict:
    with open(ARTIFACTS_DIR / "metadata.json") as f:
        return json.load(f)


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    ref = pd.read_csv(PROCESSED_DIR / "train_prepared.csv")
    curr = pd.read_csv(PROCESSED_DIR / "validation_prepared.csv")
    return ref, curr


def add_predictions(df: pd.DataFrame, pipeline, features: list[str]) -> pd.DataFrame:
    df = df.copy()
    df["prediction"] = pipeline.predict(df[features])
    return df


def build_column_mapping(metadata: dict) -> ColumnMapping:
    return ColumnMapping(
        target=metadata["target"],
        prediction="prediction",
        numerical_features=metadata["numerical_features"] + metadata["engineered_features"],
        categorical_features=metadata["categorical_features"],
    )


def run():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    metadata = load_metadata()
    pipeline = joblib.load(ARTIFACTS_DIR / "churn_pipeline.joblib")
    features = metadata["model_features"]

    ref_df, curr_df = load_datasets()
    ref_df = add_predictions(ref_df, pipeline, features)
    curr_df = add_predictions(curr_df, pipeline, features)

    column_mapping = build_column_mapping(metadata)

    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=ref_df, current_data=curr_df, column_mapping=column_mapping)
    drift_report.save_html(str(REPORTS_DIR / "data_drift.html"))
    print(f"[OK] data_drift.html saved to {REPORTS_DIR}")

    perf_report = Report(metrics=[ClassificationPreset()])
    perf_report.run(reference_data=ref_df, current_data=curr_df, column_mapping=column_mapping)
    perf_report.save_html(str(REPORTS_DIR / "classification_performance.html"))
    print(f"[OK] classification_performance.html saved to {REPORTS_DIR}")


if __name__ == "__main__":
    run()
