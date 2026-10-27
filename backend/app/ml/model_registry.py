"""Translation model registry.

Maps each supported (source, target) language pair to its *verified* Hugging Face
model identifier. Reversing a direction uses the separate reverse model - a single
model is never reused for both directions.

All identifiers and their Apache-2.0 license were confirmed live against the
Hugging Face Hub API before being pinned here.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationPair:
    source: str
    target: str
    model_id: str
    license: str = "apache-2.0"


# Human-readable language names for the languages we support.
LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "es": "Spanish",
}

# The single source of truth for supported directions.
TRANSLATION_PAIRS: dict[tuple[str, str], TranslationPair] = {
    ("en", "hi"): TranslationPair("en", "hi", "Helsinki-NLP/opus-mt-en-hi"),
    ("hi", "en"): TranslationPair("hi", "en", "Helsinki-NLP/opus-mt-hi-en"),
    ("en", "fr"): TranslationPair("en", "fr", "Helsinki-NLP/opus-mt-en-fr"),
    ("fr", "en"): TranslationPair("fr", "en", "Helsinki-NLP/opus-mt-fr-en"),
    ("en", "es"): TranslationPair("en", "es", "Helsinki-NLP/opus-mt-en-es"),
    ("es", "en"): TranslationPair("es", "en", "Helsinki-NLP/opus-mt-es-en"),
}


def is_known_language(code: str) -> bool:
    return code in LANGUAGE_NAMES


def get_pair(source: str, target: str) -> TranslationPair | None:
    return TRANSLATION_PAIRS.get((source, target))


def supported_languages() -> list[str]:
    return sorted(LANGUAGE_NAMES)
