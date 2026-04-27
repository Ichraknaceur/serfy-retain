from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
    }
