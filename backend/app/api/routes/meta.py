from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["meta"])


@router.get("/")
def root() -> dict:
    settings = get_settings()
    return {
        "product": "Serfy Retain",
        "service": settings.app_name,
        "version": settings.app_version,
        "message": "Clean foundation for a bank churn retention platform.",
        "next_modules": [
            "prediction",
            "recommendation",
            "agent",
            "monitoring",
        ],
    }
