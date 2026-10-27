"""Integration tests over the HTTP API.

Model inference is mocked at the service boundary so these run fast and offline.
They verify routing, validation, status codes, error envelope and response schema.
"""
from __future__ import annotations

import pytest

from app.schemas import SentimentResponse, TranslateResponse
from app.services import sentiment_service, translation_service

V1 = "/api/v1"


# ---- metadata / health ----

def test_health_shape(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "readiness" in body
    for key in ("api_process", "translation_model_ready", "sentiment_model_ready"):
        assert key in body["readiness"]
    # API process is up; models are lazily loaded so not falsely claimed ready.
    assert body["readiness"]["api_process"] is True


def test_languages_endpoint(client):
    r = client.get(f"{V1}/languages")
    assert r.status_code == 200
    body = r.json()
    codes = {l["code"] for l in body["languages"]}
    assert codes == {"en", "hi", "fr", "es"}
    assert body["auto_detect_supported"] is False
    assert len(body["directions"]) == 6


def test_models_endpoint(client):
    r = client.get(f"{V1}/models")
    assert r.status_code == 200
    body = r.json()
    assert len(body["translation_models"]) == 6
    assert body["sentiment_models"][0]["labels"] == ["NEGATIVE", "POSITIVE"]
    # No secret leakage.
    text = r.text.lower()
    assert "hf_token" not in text and "api_key" not in text


# ---- translate ----

def test_translate_success(client, monkeypatch):
    monkeypatch.setattr(
        translation_service,
        "translate",
        lambda text, s, t: TranslateResponse(
            source_language=s, target_language=t, translated_text="Bonjour",
            model_id="Helsinki-NLP/opus-mt-en-fr", processing_time_ms=5, warnings=[],
        ),
    )
    r = client.post(f"{V1}/translate", json={"text": "Hello", "source_language": "en", "target_language": "fr"})
    assert r.status_code == 200
    assert r.json()["translated_text"] == "Bonjour"


def test_translate_rejects_extra_fields(client):
    r = client.post(
        f"{V1}/translate",
        json={"text": "Hi", "source_language": "en", "target_language": "fr", "evil": 1},
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


def test_translate_unsupported_pair(client):
    # No service call needed: validation happens in service; use real function here.
    r = client.post(f"{V1}/translate", json={"text": "Hi", "source_language": "hi", "target_language": "fr"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "unsupported_language_pair"


def test_translate_empty_input(client):
    r = client.post(f"{V1}/translate", json={"text": "   ", "source_language": "en", "target_language": "fr"})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "empty_input"


# ---- sentiment ----

def test_sentiment_success(client, monkeypatch):
    monkeypatch.setattr(
        sentiment_service,
        "analyze",
        lambda text: SentimentResponse(
            predicted_label="positive", scores={"negative": 0.1, "positive": 0.9},
            model_id=sentiment_service.SENTIMENT_MODEL_ID, language="en",
            processing_time_ms=3, limitations="English-only", warnings=[],
        ),
    )
    r = client.post(f"{V1}/sentiment", json={"text": "I love this project"})
    assert r.status_code == 200
    assert r.json()["predicted_label"] == "positive"


def test_sentiment_empty(client):
    r = client.post(f"{V1}/sentiment", json={"text": ""})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "empty_input"


# ---- combined analyse ----

@pytest.fixture()
def patched_services(monkeypatch):
    monkeypatch.setattr(
        translation_service,
        "translate",
        lambda text, s, t: TranslateResponse(
            source_language=s, target_language=t, translated_text="J'adore ce projet",
            model_id="Helsinki-NLP/opus-mt-en-fr", processing_time_ms=4, warnings=[],
        ),
    )
    monkeypatch.setattr(
        sentiment_service,
        "analyze",
        lambda text: SentimentResponse(
            predicted_label="positive", scores={"negative": 0.05, "positive": 0.95},
            model_id=sentiment_service.SENTIMENT_MODEL_ID, language="en",
            processing_time_ms=2, limitations="English-only", warnings=[],
        ),
    )


def test_analyse_translated_target(client, patched_services):
    r = client.post(f"{V1}/analyse", json={
        "text": "I love this project", "source_language": "en",
        "target_language": "fr", "sentiment_target": "translated",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["analysed_text_origin"] == "translated"
    assert body["analysed_text"] == "J'adore ce projet"
    assert body["translation"]["translated_text"] == "J'adore ce projet"
    assert body["sentiment"]["predicted_label"] == "positive"


def test_analyse_original_target(client, patched_services, monkeypatch):
    # original path calls translation_service.validate_text (real, returns text).
    r = client.post(f"{V1}/analyse", json={
        "text": "I love this project", "source_language": "en",
        "target_language": "fr", "sentiment_target": "original",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["analysed_text_origin"] == "original"
    assert body["analysed_text"] == "I love this project"


def test_analyse_invalid_sentiment_target(client):
    r = client.post(f"{V1}/analyse", json={
        "text": "Hi", "source_language": "en", "target_language": "fr",
        "sentiment_target": "banana",
    })
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"
