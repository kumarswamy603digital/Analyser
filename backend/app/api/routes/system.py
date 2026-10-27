"""System/metadata endpoints: /health, /languages, /models."""
from __future__ import annotations

from fastapi import APIRouter

from ...core.config import settings
from ...ml.model_metadata import sentiment_models, translation_models
from ...schemas import HealthResponse, LanguagesResponse, ModelsResponse, Readiness
from ...services import language_service
from ...services import sentiment_service, translation_service

health_router = APIRouter(tags=["system"])
router = APIRouter(tags=["system"])


@health_router.get("/health", response_model=HealthResponse, summary="Health and readiness")
def health() -> HealthResponse:
    """Distinguish API process availability from per-model readiness.

    Model readiness reflects actual load state: a model that has not loaded yet, or
    that failed to load, is reported as not ready (never falsely ready).
    """
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        readiness=Readiness(
            api_process=True,
            translation_model_ready=translation_service.translation_ready(),
            sentiment_model_ready=sentiment_service.sentiment_ready(),
        ),
    )


@router.get("/languages", response_model=LanguagesResponse)
def languages() -> LanguagesResponse:
    return language_service.get_languages()


@router.get("/models", response_model=ModelsResponse)
def models() -> ModelsResponse:
    return ModelsResponse(
        translation_models=translation_models(),
        sentiment_models=sentiment_models(),
    )
