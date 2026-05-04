from fastapi import APIRouter

from app.core.config import get_settings
from app.services.model_loader import get_model_artifacts_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    artifacts = get_model_artifacts_service()
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
        "model_artifacts_ready": artifacts.is_ready(),
    }
