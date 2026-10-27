"""Static model metadata used by /api/v1/models and the About page.

Limitations text is intentionally cautious and reflects what the models actually
support, not marketing claims.
"""
from __future__ import annotations

from ..schemas import ModelInfo
from .model_registry import TRANSLATION_PAIRS

SENTIMENT_MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
SENTIMENT_LABELS = ["NEGATIVE", "POSITIVE"]
SENTIMENT_LICENSE = "apache-2.0"
SENTIMENT_LIMITATIONS = (
    "English-only binary sentiment classifier (positive/negative) fine-tuned on "
    "SST-2. It does not output a neutral class, does not support other languages, "
    "and its scores are model confidences, not guaranteed probabilities of being "
    "correct. Predictions may be wrong, especially for sarcasm, negation-heavy or "
    "out-of-domain text."
)


def translation_models() -> list[ModelInfo]:
    models: list[ModelInfo] = []
    for pair in TRANSLATION_PAIRS.values():
        models.append(
            ModelInfo(
                model_id=pair.model_id,
                task="translation",
                supported_languages=[pair.source, pair.target],
                labels=None,
                license=pair.license,
                limitations=(
                    f"OPUS-MT {pair.source}->{pair.target} direction model. Quality "
                    "varies by domain and sentence length; long or out-of-domain text "
                    "may be mistranslated. This direction uses its own model and is not "
                    "the reverse model."
                ),
            )
        )
    return models


def sentiment_models() -> list[ModelInfo]:
    return [
        ModelInfo(
            model_id=SENTIMENT_MODEL_ID,
            task="text-classification",
            supported_languages=["en"],
            labels=SENTIMENT_LABELS,
            license=SENTIMENT_LICENSE,
            limitations=SENTIMENT_LIMITATIONS,
        )
    ]
