"""Unit tests for the model registry, metadata and language service."""
from __future__ import annotations

from app.ml import model_registry as reg
from app.ml.model_metadata import sentiment_models, translation_models
from app.services import language_service


def test_reverse_direction_uses_distinct_models():
    en_hi = reg.get_pair("en", "hi").model_id
    hi_en = reg.get_pair("hi", "en").model_id
    assert en_hi != hi_en


def test_all_pairs_have_verified_ids():
    for pair in reg.TRANSLATION_PAIRS.values():
        assert pair.model_id.startswith("Helsinki-NLP/opus-mt-")
        assert pair.license == "apache-2.0"


def test_known_language_check():
    assert reg.is_known_language("en")
    assert not reg.is_known_language("de")


def test_languages_response_only_supported_pairs():
    resp = language_service.get_languages()
    codes = {l.code for l in resp.languages}
    assert codes == {"en", "hi", "fr", "es"}
    # Every advertised direction must exist in the registry.
    for d in resp.directions:
        assert reg.get_pair(d.source, d.target) is not None
    assert resp.auto_detect_supported is False


def test_models_metadata_shape():
    t = translation_models()
    s = sentiment_models()
    assert len(t) == len(reg.TRANSLATION_PAIRS)
    assert len(s) == 1
    assert s[0].labels == ["NEGATIVE", "POSITIVE"]
    assert s[0].supported_languages == ["en"]
