from fastapi import APIRouter, HTTPException

from app.schemas.prediction import ModelInfoResponse
from app.services.model_loader import get_model_artifacts_service

router = APIRouter(tags=["model"])


@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_info() -> ModelInfoResponse:
    service = get_model_artifacts_service()
    if not service.is_ready():
        raise HTTPException(status_code=503, detail="Model artifacts are not available yet.")

    metadata = service.load_metadata()

    return ModelInfoResponse(
        model_name=metadata["model_name"],
        target=metadata["target"],
        categorical_features=metadata["categorical_features"],
        numerical_features=metadata["numerical_features"],
        engineered_features=metadata["engineered_features"],
        model_features=metadata["model_features"],
        transformed_feature_count=metadata["transformed_feature_count"],
        metrics=metadata["metrics"],
        artifacts_dir=str(service.artifacts_dir),
    )
