from fastapi import APIRouter, HTTPException

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.model_loader import get_model_artifacts_service

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    service = get_model_artifacts_service()
    if not service.is_ready():
        raise HTTPException(status_code=503, detail="Model artifacts are not available yet.")

    prediction = service.predict(payload.model_dump())
    return PredictionResponse(**prediction)
