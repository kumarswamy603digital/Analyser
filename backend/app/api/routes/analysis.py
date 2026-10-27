"""Analysis endpoints: /translate, /sentiment, /analyse."""
from __future__ import annotations

from fastapi import APIRouter

from ...schemas import (
    AnalyseRequest,
    AnalyseResponse,
    SentimentRequest,
    SentimentResponse,
    SentimentTarget,
    TranslateRequest,
    TranslateResponse,
)
from ...services import sentiment_service, translation_service

router = APIRouter(tags=["analysis"])


@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest) -> TranslateResponse:
    return translation_service.translate(req.text, req.source_language, req.target_language)


@router.post("/sentiment", response_model=SentimentResponse)
def sentiment(req: SentimentRequest) -> SentimentResponse:
    return sentiment_service.analyze(req.text)


@router.post("/analyse", response_model=AnalyseResponse)
def analyse(req: AnalyseRequest) -> AnalyseResponse:
    """Combined workflow: translate, then analyse the explicitly selected text."""
    translation = translation_service.translate(
        req.text, req.source_language, req.target_language
    )

    if req.sentiment_target == SentimentTarget.original:
        analysed_text = translation_service.validate_text(req.text)
        origin = SentimentTarget.original
    else:
        analysed_text = translation.translated_text
        origin = SentimentTarget.translated

    sentiment_result = sentiment_service.analyze(analysed_text)

    # Honest caveat: the sentiment model is English-only. Warn if the analysed
    # text is not English (e.g. analysing a non-English original text).
    if origin == SentimentTarget.original and req.source_language.lower() != "en":
        sentiment_result.warnings.append(
            "The sentiment model is English-only; analysing non-English original "
            "text may produce unreliable results."
        )

    return AnalyseResponse(
        translation=translation,
        sentiment=sentiment_result,
        analysed_text=analysed_text,
        analysed_text_origin=origin,
    )
