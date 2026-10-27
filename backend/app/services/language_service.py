"""Language service: exposes only the pairs the registry actually supports."""
from __future__ import annotations

from ..ml import model_registry
from ..schemas import LanguageInfo, LanguagesResponse, SupportedPair


def get_languages() -> LanguagesResponse:
    languages = [
        LanguageInfo(code=code, name=model_registry.LANGUAGE_NAMES[code])
        for code in model_registry.supported_languages()
    ]
    directions = [
        SupportedPair(source=p.source, target=p.target, model_id=p.model_id)
        for p in model_registry.TRANSLATION_PAIRS.values()
    ]
    return LanguagesResponse(
        languages=languages,
        directions=directions,
        auto_detect_supported=False,
    )
