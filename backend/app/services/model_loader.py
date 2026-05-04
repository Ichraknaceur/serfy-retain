from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.core.config import get_settings
from training.data_contract import MODEL_FEATURES
from training.preprocess import prepare_training_frame


class ModelArtifactsService:
    def __init__(self, artifacts_dir: Path) -> None:
        self.artifacts_dir = artifacts_dir
        self.pipeline_path = artifacts_dir / "churn_pipeline.joblib"
        self.metadata_path = artifacts_dir / "metadata.json"
        self.feature_names_path = artifacts_dir / "feature_names.json"

    def is_ready(self) -> bool:
        return (
            self.pipeline_path.exists()
            and self.metadata_path.exists()
            and self.feature_names_path.exists()
        )

    def _ensure_ready(self) -> None:
        if not self.is_ready():
            raise FileNotFoundError(
                f"Model artifacts are missing in {self.artifacts_dir}. Run the training pipeline first."
            )

    @lru_cache(maxsize=1)
    def load_pipeline(self):
        self._ensure_ready()
        return joblib.load(self.pipeline_path)

    @lru_cache(maxsize=1)
    def load_metadata(self) -> dict[str, Any]:
        self._ensure_ready()
        return json.loads(self.metadata_path.read_text(encoding="utf-8"))

    @lru_cache(maxsize=1)
    def load_feature_names(self) -> list[str]:
        self._ensure_ready()
        return json.loads(self.feature_names_path.read_text(encoding="utf-8"))

    def predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        pipeline = self.load_pipeline()
        metadata = self.load_metadata()

        raw_df = pd.DataFrame([payload])
        prepared_df = prepare_training_frame(raw_df, require_target=False)
        feature_frame = prepared_df[MODEL_FEATURES].copy()

        churn_probability = float(pipeline.predict_proba(feature_frame)[0][1])
        predicted_class = int(pipeline.predict(feature_frame)[0])

        if churn_probability < 0.3:
            risk_level = "low"
        elif churn_probability < 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"

        return {
            "churn_probability": churn_probability,
            "risk_level": risk_level,
            "predicted_class": predicted_class,
            "model_name": metadata.get("model_name", "unknown"),
        }


@lru_cache(maxsize=1)
def get_model_artifacts_service() -> ModelArtifactsService:
    settings = get_settings()
    return ModelArtifactsService(settings.resolved_artifacts_dir())
