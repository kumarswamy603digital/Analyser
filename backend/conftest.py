"""Shared pytest fixtures/helpers.

Fast tests never import torch or download models: inference is mocked. A separate
`slow` marked test exercises real model inference when the runtime is available.
"""
from __future__ import annotations

import os
import sys

# Ensure the backend directory is importable as the `app` package.
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Keep model cache + downloads inside the repo during tests.
os.environ.setdefault("HF_HOME", os.path.join(BACKEND_DIR, "HF_HOME"))

import pytest  # noqa: E402


@pytest.fixture()
def client():
    """FastAPI TestClient with a fresh app per test."""
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c
