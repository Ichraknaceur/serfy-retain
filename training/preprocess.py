from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from training.config import get_training_config
from training.data_contract import (
    CATEGORICAL_FEATURES,
    ENGINEERED_FEATURES,
    ID_COLUMN,
    MODEL_FEATURES,
    NUMERICAL_FEATURES,
    RAW_TO_CANONICAL_COLUMN_MAP,
    TARGET_COLUMN,
    TARGET_VALUE_MAP,
)


def normalize_column_name(column: str) -> str:
    column = column.strip()
    if column in RAW_TO_CANONICAL_COLUMN_MAP:
        return RAW_TO_CANONICAL_COLUMN_MAP[column]

    column = re.sub(r"[^a-zA-Z0-9]+", "_", column).strip("_")
    return column.lower()


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {column: normalize_column_name(column) for column in df.columns}
    return df.rename(columns=renamed)


def drop_unused_columns(df: pd.DataFrame) -> pd.DataFrame:
    drop_columns = [
        column
        for column in df.columns
        if column.startswith("naive_bayes_classifier_attrition_flag")
        or column.startswith("avg_utilization_ratio_")
    ]

    if drop_columns:
        return df.drop(columns=drop_columns)

    return df


def clean_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    if "marital_status" in cleaned.columns:
        cleaned["marital_status"] = cleaned["marital_status"].replace("Unknown", "Married")

    if "income_category" in cleaned.columns:
        cleaned["income_category"] = cleaned["income_category"].replace("Unknown", "Less than $40K")

    return cleaned


def encode_target(df: pd.DataFrame) -> pd.DataFrame:
    if TARGET_COLUMN not in df.columns:
        return df

    encoded = df.copy()
    encoded[TARGET_COLUMN] = encoded[TARGET_COLUMN].map(TARGET_VALUE_MAP)
    return encoded


def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    filled = df.copy()

    for column in CATEGORICAL_FEATURES:
        if column in filled.columns:
            filled[column] = filled[column].fillna("Unknown")

    for column in NUMERICAL_FEATURES + ENGINEERED_FEATURES:
        if column in filled.columns:
            filled[column] = filled[column].fillna(0.0)

    return filled


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.replace(0, pd.NA)
    result = numerator / denominator
    return result.fillna(0.0)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    engineered = df.copy()

    if {"months_on_book", "customer_age"}.issubset(engineered.columns):
        engineered["tenure_per_age"] = _safe_divide(
            engineered["months_on_book"],
            engineered["customer_age"] * 12,
        )

    if {"avg_utilization_ratio", "customer_age"}.issubset(engineered.columns):
        engineered["utilization_per_age"] = _safe_divide(
            engineered["avg_utilization_ratio"],
            engineered["customer_age"],
        )

    if {"credit_limit", "customer_age"}.issubset(engineered.columns):
        engineered["credit_limit_per_age"] = _safe_divide(
            engineered["credit_limit"],
            engineered["customer_age"],
        )

    if {"total_trans_amt", "credit_limit"}.issubset(engineered.columns):
        engineered["total_trans_amt_per_credit_limit"] = _safe_divide(
            engineered["total_trans_amt"],
            engineered["credit_limit"],
        )

    if {"total_trans_ct", "credit_limit"}.issubset(engineered.columns):
        engineered["total_trans_ct_per_credit_limit"] = _safe_divide(
            engineered["total_trans_ct"],
            engineered["credit_limit"],
        )

    for column in ENGINEERED_FEATURES:
        if column not in engineered.columns:
            engineered[column] = 0.0

    return engineered


def prepare_training_frame(df: pd.DataFrame, require_target: bool = True) -> pd.DataFrame:
    prepared = standardize_columns(df)
    prepared = drop_unused_columns(prepared)
    prepared = clean_categorical_values(prepared)

    if require_target and TARGET_COLUMN not in prepared.columns:
        raise ValueError(
            f"Missing required target column: {TARGET_COLUMN}. "
            "Check the source dataset schema before training."
        )

    prepared = encode_target(prepared)
    prepared = add_engineered_features(prepared)
    prepared = fill_missing_values(prepared)

    expected_columns = list(dict.fromkeys([ID_COLUMN, TARGET_COLUMN] + MODEL_FEATURES))
    for column in expected_columns:
        if column not in prepared.columns:
            if column == TARGET_COLUMN:
                continue
            prepared[column] = 0 if column in NUMERICAL_FEATURES + ENGINEERED_FEATURES else "Unknown"

    available_columns = [column for column in expected_columns if column in prepared.columns]
    prepared = prepared[available_columns].copy()

    if require_target and prepared[TARGET_COLUMN].isna().any():
        raise ValueError("Target column contains unmapped values. Check the source dataset labels.")

    return prepared


def split_features_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    return df[MODEL_FEATURES].copy(), df[TARGET_COLUMN].astype(int)


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES + ENGINEERED_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def create_train_validation_split(
    df: pd.DataFrame,
    test_size: float,
    random_state: int,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[TARGET_COLUMN],
    )


def write_preprocessing_outputs(train_df: pd.DataFrame, valid_df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(output_dir / "train_prepared.csv", index=False)
    valid_df.to_csv(output_dir / "validation_prepared.csv", index=False)

    schema_summary = {
        "id_column": ID_COLUMN,
        "target_column": TARGET_COLUMN,
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "engineered_features": ENGINEERED_FEATURES,
        "model_features": MODEL_FEATURES,
        "train_rows": len(train_df),
        "validation_rows": len(valid_df),
    }

    with open(output_dir / "schema_summary.json", "w", encoding="utf-8") as file:
        json.dump(schema_summary, file, indent=2)


def main() -> None:
    config = get_training_config()
    parser = argparse.ArgumentParser(description="Prepare the churn dataset for training.")
    parser.add_argument("--input", type=Path, default=config.raw_data_path)
    parser.add_argument("--output-dir", type=Path, default=config.processed_data_dir)
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {args.input}. "
            "Place the CSV file there or override it with RAW_DATA_PATH/--input."
        )

    raw_df = pd.read_csv(args.input)
    prepared_df = prepare_training_frame(raw_df, require_target=True)
    train_df, valid_df = create_train_validation_split(
        prepared_df,
        test_size=config.test_size,
        random_state=config.random_state,
    )
    write_preprocessing_outputs(train_df, valid_df, args.output_dir)

    print("Prepared dataset written successfully.")
    print(f"Train rows: {len(train_df)}")
    print(f"Validation rows: {len(valid_df)}")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()
