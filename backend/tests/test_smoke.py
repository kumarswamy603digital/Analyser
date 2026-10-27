"""Real-model smoke tests (tagged `slow`).

These download/use actual Hugging Face weights and run genuine CPU inference.
They are deselected by default (see pytest.ini addopts) and run explicitly with:
    python -m pytest -m slow

They require a working torch runtime (Microsoft Visual C++ Redistributable present).
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.slow


def test_real_sentiment_inference():
    from app.services import sentiment_service as ss

    pos = ss.analyze("This is absolutely wonderful and I loved every minute.")
    neg = ss.analyze("This is terrible and a complete waste of time.")
    assert set(pos.scores.keys()) == {"positive", "negative"}
    assert pos.predicted_label == "positive"
    assert neg.predicted_label == "negative"
    assert pos.processing_time_ms >= 0


def test_real_translation_inference_en_fr():
    from app.services import translation_service as ts

    resp = ts.translate("I love this project", "en", "fr")
    assert resp.model_id == "Helsinki-NLP/opus-mt-en-fr"
    assert resp.translated_text  # non-empty real output
    assert resp.source_language == "en"
    assert resp.target_language == "fr"
