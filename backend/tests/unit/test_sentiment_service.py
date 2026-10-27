"""Unit tests for the sentiment service (inference mocked - no torch/network)."""
from __future__ import annotations

import pytest

from app.core.exceptions import EmptyInputError, InferenceError, InputTooLongError
from app.services import sentiment_service as ss


def test_validate_rejects_empty():
    with pytest.raises(EmptyInputError):
        ss.validate_text("")


def test_validate_rejects_too_long():
    with pytest.raises(InputTooLongError) as exc:
        ss.validate_text("a" * (ss.settings.max_input_chars + 1))
    assert exc.value.status_code == 413


def test_interpret_positive_mapping():
    # HF SST-2 model uses {0: 'NEGATIVE', 1: 'POSITIVE'}.
    id2label = {0: "NEGATIVE", 1: "POSITIVE"}
    resp = ss._interpret(id2label, [0.05, 0.95], duration_ms=12)
    assert resp.predicted_label == "positive"
    assert resp.scores["positive"] == pytest.approx(0.95)
    assert resp.scores["negative"] == pytest.approx(0.05)


def test_interpret_negative_mapping():
    id2label = {0: "NEGATIVE", 1: "POSITIVE"}
    resp = ss._interpret(id2label, [0.8, 0.2], duration_ms=9)
    assert resp.predicted_label == "negative"
    assert resp.scores["negative"] == pytest.approx(0.8)


def test_interpret_includes_limitations_and_warning():
    id2label = {0: "NEGATIVE", 1: "POSITIVE"}
    resp = ss._interpret(id2label, [0.1, 0.9], duration_ms=1)
    assert "English-only" in resp.limitations
    assert resp.warnings
    assert resp.model_id == ss.SENTIMENT_MODEL_ID


def test_analyze_success_with_mocked_inference(monkeypatch):
    monkeypatch.setattr(ss, "_load", lambda: {"fake": True})
    monkeypatch.setattr(
        ss, "_raw_probs", lambda entry, text: ({0: "NEGATIVE", 1: "POSITIVE"}, [0.1, 0.9])
    )
    resp = ss.analyze("I love this")
    assert resp.predicted_label == "positive"
    assert resp.processing_time_ms >= 0


def test_analyze_inference_failure(monkeypatch):
    monkeypatch.setattr(ss, "_load", lambda: {"fake": True})

    def boom(entry, text):
        raise RuntimeError("model blew up")

    monkeypatch.setattr(ss, "_raw_probs", boom)
    with pytest.raises(InferenceError):
        ss.analyze("hello")


def test_analyze_model_init_failure(monkeypatch):
    def boom():
        raise InferenceError("cannot load")

    monkeypatch.setattr(ss, "_load", boom)
    with pytest.raises(InferenceError):
        ss.analyze("hello")
