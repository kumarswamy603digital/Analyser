"""Translation service using Hugging Face OPUS-MT models (real inference).

Design:
- Models are loaded lazily per direction and cached in memory (never reloaded per
  request). Loading is guarded by a per-model lock so simultaneous requests cannot
  trigger duplicate initialization.
- CPU by default; optional GPU if configured and available.
- The heavy transformers/torch imports are done inside functions so the module can
  be imported (for metadata/tests) without downloading or loading anything.
"""
from __future__ import annotations

import threading
import time

from ..core.config import settings
from ..core.exceptions import (
    EmptyInputError,
    InferenceError,
    InputTooLongError,
    InvalidLanguageError,
    UnsupportedPairError,
)
from ..core.logging import get_logger
from ..ml import model_registry
from ..schemas import TranslateResponse

logger = get_logger("app.services.translation")

# model_id -> {"tokenizer": ..., "model": ...}
_CACHE: dict[str, dict] = {}
_CACHE_LOCK = threading.Lock()
_LOAD_LOCKS: dict[str, threading.Lock] = {}
_LOAD_ERRORS: dict[str, str] = {}


def _lock_for(model_id: str) -> threading.Lock:
    with _CACHE_LOCK:
        return _LOAD_LOCKS.setdefault(model_id, threading.Lock())


def _resolve_device() -> str:
    if settings.device == "cuda":
        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"
        except Exception:  # pragma: no cover - fallback path
            pass
    return "cpu"


def _load(model_id: str) -> dict:
    """Load tokenizer+model for a direction once, thread-safely, and cache it."""
    with _CACHE_LOCK:
        cached = _CACHE.get(model_id)
    if cached is not None:
        return cached

    lock = _lock_for(model_id)
    with lock:
        # Double-check after acquiring the per-model lock.
        with _CACHE_LOCK:
            cached = _CACHE.get(model_id)
        if cached is not None:
            return cached

        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

            device = _resolve_device()
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                token=(settings.hf_token or None),
            )
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_id,
                token=(settings.hf_token or None),
            )
            model.to(device)
            model.eval()
            entry = {"tokenizer": tokenizer, "model": model, "device": device}
            with _CACHE_LOCK:
                _CACHE[model_id] = entry
                _LOAD_ERRORS.pop(model_id, None)
            logger.info("Loaded translation model %s on %s", model_id, device)
            return entry
        except Exception as exc:  # noqa: BLE001
            _LOAD_ERRORS[model_id] = str(exc)
            logger.exception("Failed to load translation model %s", model_id)
            raise InferenceError(
                "Translation model failed to load. It may not be downloaded yet or "
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


def _validate_pair(source: str, target: str) -> model_registry.TranslationPair:
    src = (source or "").strip().lower()
    tgt = (target or "").strip().lower()
    if not model_registry.is_known_language(src) or not model_registry.is_known_language(tgt):
        raise InvalidLanguageError(
            details={"source_language": src, "target_language": tgt}
        )
    if src == tgt:
        raise UnsupportedPairError(
            "Source and target language are identical.",
            details={"source_language": src, "target_language": tgt},
        )
    pair = model_registry.get_pair(src, tgt)
    if pair is None:
        raise UnsupportedPairError(
            details={"source_language": src, "target_language": tgt},
        )
    return pair


def is_model_loaded(model_id: str) -> bool:
    with _CACHE_LOCK:
        return model_id in _CACHE


def translation_ready() -> bool:
    """Ready if at least one direction model has loaded and none failed fatally.

    Honest semantics: a model that has not been loaded yet is simply not ready;
    a model whose load raised is recorded and prevents a false 'ready'.
    """
    with _CACHE_LOCK:
        return bool(_CACHE) and not _LOAD_ERRORS


def _run_inference(entry: dict, text: str) -> str:
    """Perform the actual (torch) generation for one direction. Isolated for testing."""
    import torch

    tokenizer, model, device = entry["tokenizer"], entry["model"], entry["device"]
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.inference_mode():
        generated = model.generate(
            **inputs,
            num_beams=4,
            max_length=min(512, max(40, int(len(text) * 2.5) + 16)),
            no_repeat_ngram_size=3,
        )
    return tokenizer.decode(generated[0], skip_special_tokens=True).strip()


def translate(text: str, source: str, target: str) -> TranslateResponse:
    clean = validate_text(text)
    pair = _validate_pair(source, target)

    entry = _load(pair.model_id)

    start = time.perf_counter()
    try:
        translated = _run_inference(entry, clean)
    except InferenceError:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Translation inference failed")
        raise InferenceError("Translation inference failed.") from exc

    duration_ms = int((time.perf_counter() - start) * 1000)
    warnings: list[str] = []
    if not translated:
        warnings.append("Model returned an empty translation.")

    return TranslateResponse(
        source_language=pair.source,
        target_language=pair.target,
        translated_text=translated,
        model_id=pair.model_id,
        processing_time_ms=duration_ms,
        warnings=warnings,
    )
