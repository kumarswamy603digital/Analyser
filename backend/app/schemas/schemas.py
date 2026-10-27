"""Pydantic request/response schemas for the API."""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SentimentTarget(str, Enum):
    """Explicit choice for the combined workflow: which text gets analysed."""

    original = "original"
    translated = "translated"


class LanguageInfo(BaseModel):
    code: str
    name: str


class SupportedPair(BaseModel):
    source: str
    target: str
    model_id: str


class LanguagesResponse(BaseModel):
    languages: list[LanguageInfo]
    directions: list[SupportedPair]
    auto_detect_supported: bool = False


class ModelInfo(BaseModel):
    model_id: str
    task: str
    supported_languages: list[str]
    labels: list[str] | None = None
    license: str
    limitations: str


class ModelsResponse(BaseModel):
    translation_models: list[ModelInfo]
    sentiment_models: list[ModelInfo]


class Readiness(BaseModel):
    api_process: bool = True
    translation_model_ready: bool
    sentiment_model_ready: bool


class HealthResponse(BaseModel):
    status: str
    version: str
    readiness: Readiness


class TranslateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="Source text to translate.")
    source_language: str = Field(..., min_length=2, max_length=8)
    target_language: str = Field(..., min_length=2, max_length=8)


class TranslateResponse(BaseModel):
    source_language: str
    target_language: str
    translated_text: str
    model_id: str
    processing_time_ms: int
    warnings: list[str] = Field(default_factory=list)


class SentimentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="Text to classify.")


class SentimentResponse(BaseModel):
    predicted_label: str
    scores: dict[str, float]
    model_id: str
    language: str = "en"
    processing_time_ms: int
    limitations: str
    warnings: list[str] = Field(default_factory=list)


class AnalyseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    source_language: str = Field(..., min_length=2, max_length=8)
    target_language: str = Field(..., min_length=2, max_length=8)
    sentiment_target: SentimentTarget = SentimentTarget.translated


class AnalyseResponse(BaseModel):
    translation: TranslateResponse
    sentiment: SentimentResponse
    analysed_text: str
    analysed_text_origin: SentimentTarget
