"""Unit tests for the translation service (inference mocked - no torch/network)."""
from __future__ import annotations

import pytest

from app.core.exceptions import (
    EmptyInputError,
    InferenceError,
    InputTooLongError,
    InvalidLanguageError,
    UnsupportedPairError,
)
from app.services import translation_service as ts


def test_validate_rejects_empty():
    with pytest.raises(EmptyInputError):
        ts.validate_text("")


def test_validate_rejects_whitespace_only():
    with pytest.raises(EmptyInputError):
        ts.validate_text("   \n\t ")


def test_validate_rejects_too_long():
    long_text = "a" * (ts.settings.max_input_chars + 1)
    with pytest.raises(InputTooLongError) as exc:
        ts.validate_text(long_text)
    assert exc.value.status_code == 413


def test_validate_returns_stripped():
    assert ts.validate_text("  hello  ") == "hello"


def test_pair_unknown_language():
    with pytest.raises(InvalidLanguageError):
        ts._validate_pair("en", "zz")


def test_pair_identical_languages():
    with pytest.raises(UnsupportedPairError):
        ts._validate_pair("en", "en")


def test_pair_unsupported_direction():
    # Both languages are known but this direction is not in the registry.
    with pytest.raises(UnsupportedPairError):
        ts._validate_pair("hi", "fr")


def test_pair_valid():
    pair = ts._validate_pair("en", "fr")
    assert pair.model_id == "Helsinki-NLP/opus-mt-en-fr"


def test_translate_success_with_mocked_inference(monkeypatch):
    monkeypatch.setattr(ts, "_load", lambda model_id: {"fake": True})
    monkeypatch.setattr(ts, "_run_inference", lambda entry, text: "Bonjour")

    resp = ts.translate("Hello", "en", "fr")
    assert resp.translated_text == "Bonjour"
    assert resp.model_id == "Helsinki-NLP/opus-mt-en-fr"
    assert resp.source_language == "en"
    assert resp.target_language == "fr"
    assert resp.processing_time_ms >= 0
    assert resp.warnings == []


def test_translate_empty_model_output_adds_warning(monkeypatch):
    monkeypatch.setattr(ts, "_load", lambda model_id: {"fake": True})
    monkeypatch.setattr(ts, "_run_inference", lambda entry, text: "")

    resp = ts.translate("Hello", "en", "fr")
    assert resp.translated_text == ""
    assert resp.warnings


def test_translate_inference_failure_maps_to_inference_error(monkeypatch):
    monkeypatch.setattr(ts, "_load", lambda model_id: {"fake": True})

    def boom(entry, text):
        raise RuntimeError("gpu exploded")

    monkeypatch.setattr(ts, "_run_inference", boom)
    with pytest.raises(InferenceError):
        ts.translate("Hello", "en", "fr")


def test_translate_model_init_failure(monkeypatch):
    def boom(model_id):
        raise InferenceError("cannot load")

    monkeypatch.setattr(ts, "_load", boom)
    with pytest.raises(InferenceError):
        ts.translate("Hello", "en", "fr")
