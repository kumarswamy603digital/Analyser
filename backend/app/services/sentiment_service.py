"""Sentiment analysis service using DistilBERT SST-2 (real inference).

Loads the model lazily + thread-safely and caches it. Runs under torch.inference_mode
to avoid unnecessary memory/gradient tracking. Returns the model's actual scores
(softmax over the two logits) and the predicted label.
"""
from __future__ import annotations

import threading
import time

from ..core.config import settings
from ..core.exceptions import EmptyInputError, InferenceError, InputTooLongError
from ..core.logging import get_logger
from ..ml.model_metadata import (
    SENTIMENT_LIMITATIONS,
    SENTIMENT_MODEL_ID,
)
from ..schemas import SentimentResponse

logger = get_logger("app.services.sentiment")

_CACHE: dict | None = None
_LOAD_LOCK = threading.Lock()
_LOAD_ERROR: str | None = None

# Map raw model labels to friendly, stable readable labels.
LABEL_MAP = {"NEGATIVE": "negative", "POSITIVE": "positive"}


def _resolve_device() -> str:
    if settings.device == "cuda":
        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"
        except Exception:  # pragma: no cover
            pass
    return "cpu"


def _load() -> dict:
    global _CACHE, _LOAD_ERROR
    if _CACHE is not None:
        return _CACHE
    with _LOAD_LOCK:
        if _CACHE is not None:
            return _CACHE
        try:
            import torch
            from transformers import AutoModelForSequenceClassification, AutoTokenizer

            device = _resolve_device()
            tokenizer = AutoTokenizer.from_pretrained(
                SENTIMENT_MODEL_ID, token=(settings.hf_token or None)
            )
            model = AutoModelForSequenceClassification.from_pretrained(
                SENTIMENT_MODEL_ID, token=(settings.hf_token or None)
            )
            model.to(device)
            model.eval()
            _CACHE = {
                "tokenizer": tokenizer,
                "model": model,
                "device": device,
                "id2label": model.config.id2label,
                "torch": torch,
            }
            _LOAD_ERROR = None
            logger.info("Loaded sentiment model %s on %s", SENTIMENT_MODEL_ID, device)
            return _CACHE
        except Exception as exc:  # noqa: BLE001
            _LOAD_ERROR = str(exc)
            logger.exception("Failed to load sentiment model")
            raise InferenceError(
                "Sentiment model failed to load. It may not be downloaded yet or "
                "the network is unavailable."
            ) from exc


def validate_text(text: str) -> str:
    stripped = (text or "").strip()
    if not stripped:
        raise EmptyInputError()
    if len(stripped) > settings.max_input_chars:
        raise InputTooLongError(
            f"Input exceeds maximum of {settings.max_input_chars} characters.",
            status_code=413,
            details={"max_chars": settings.max_input_chars},
        )
    return stripped


def model_loaded() -> bool:
    return _CACHE is not None


def sentiment_ready() -> bool:
    # Not ready if it has never loaded AND has not failed; a failed load keeps it false.
    return _CACHE is not None and _LOAD_ERROR is None


def _raw_probs(entry: dict, text: str) -> tuple[dict, list[float]]:
    """Run torch inference and return (id2label, ordered probability list)."""
    torch = entry["torch"]
    tokenizer, model, device, id2label = (
        entry["tokenizer"],
        entry["model"],
        entry["device"],
        entry["id2label"],
    )
    # Truncation policy: max 512 tokens, right-truncated by the tokenizer.
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.inference_mode():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits[0], dim=-1)
    ordered = [float(probs[pos].item()) for pos in range(len(id2label))]
    return id2label, ordered


def _interpret(id2label: dict, probs: list[float], duration_ms: int) -> SentimentResponse:
    """Pure label/score interpretation (no torch) - maps model labels to readable ones."""
    scores: dict[str, float] = {}
    ordered_keys = sorted(id2label)
    for pos, idx in enumerate(ordered_keys):
        raw = str(id2label[idx]).upper()
        friendly = LABEL_MAP.get(raw, raw.lower())
        scores[friendly] = round(probs[pos], 6)

    predicted_pos = max(range(len(probs)), key=lambda i: probs[i])
    raw_pred = str(id2label[ordered_keys[predicted_pos]]).upper()
    predicted_label = LABEL_MAP.get(raw_pred, raw_pred.lower())

    return SentimentResponse(
        predicted_label=predicted_label,
        scores=scores,
        model_id=SENTIMENT_MODEL_ID,
        language="en",
        processing_time_ms=duration_ms,
        limitations=SENTIMENT_LIMITATIONS,
        warnings=["Scores are model confidences for a 2-class English model, "
                  "not guaranteed probabilities of real-world correctness."],
    )


def analyze(text: str) -> SentimentResponse:
    clean = validate_text(text)
    entry = _load()

    start = time.perf_counter()
    try:
        id2label, probs = _raw_probs(entry, clean)
    except InferenceError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Sentiment inference failed")
        raise InferenceError("Sentiment inference failed.") from exc

    duration_ms = int((time.perf_counter() - start) * 1000)
    return _interpret(id2label, probs, duration_ms)
