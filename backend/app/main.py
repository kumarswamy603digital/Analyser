"""FastAPI application entrypoint.

Run (from backend/):
    python -m uvicorn app.main:app --reload
"""
from __future__ import annotations

import os

from .core.config import settings

# Make the model cache configurable via env before transformers is imported.
os.environ.setdefault("HF_HOME", settings.hf_home)

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import APIRouter, FastAPI, Request  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from .api.routes import analysis, system  # noqa: E402
from .core.exceptions import register_exception_handlers  # noqa: E402
from .core.logging import configure_logging, get_logger, new_request_id  # noqa: E402

logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    logger.info(
        "Starting %s v%s (device=%s, CORS=%s)",
        settings.app_name,
        settings.app_version,
        settings.device,
        settings.cors_origin_list,
    )
    # Models are intentionally lazy-loaded on first use so startup stays fast and
    # the app can report model readiness accurately. No preload unless requested.
    if os.environ.get("PRELOAD_MODELS", "").lower() in {"1", "true", "yes"}:
        try:
            from .services import sentiment_service

            sentiment_service._load()
            logger.info("Preloaded sentiment model on startup")
        except Exception:  # noqa: BLE001
            logger.warning("Sentiment preload failed (continuing; lazy load will retry)")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI translator (OPUS-MT) and English sentiment analyser (DistilBERT SST-2) "
        "with a combined analysis workflow. Real model inference; no paid API keys."
    ),
    lifespan=lifespan,
)

# CORS from environment configuration only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.middleware("http")
async def correlation_id(request: Request, call_next):
    rid = new_request_id()
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response


# /health lives at the root; the rest are versioned under /api/v1.
app.include_router(system.health_router)

v1 = APIRouter(prefix=settings.api_v1_prefix)
v1.include_router(system.router)
v1.include_router(analysis.router)
app.include_router(v1)


@app.get("/", tags=["system"], include_in_schema=False)
def root() -> dict:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }
