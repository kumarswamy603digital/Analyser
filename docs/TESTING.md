# Testing Documentation

## Backend Tests

### Fast tests (unit + integration, inference mocked)

```powershell
cd backend
.venv\Scripts\python.exe -m pytest -v
```

These do NOT require torch, model downloads, or the VC++ Redistributable. They
verify validation, error handling, response schemas, routing, and label mapping.

**Actual result (2026-10-27): 37 passed, 2 deselected, 1.21s**

- `tests/unit/test_translation_service.py` — 9 tests: empty/whitespace/too-long, invalid lang, unsupported pair, valid pair, mocked success, empty output warning, inference failure, init failure.
- `tests/unit/test_sentiment_service.py` — 8 tests: empty/too-long, positive/negative label mapping, limitations/warnings present, mocked success, inference failure, init failure.
- `tests/unit/test_registry.py` — 5 tests: distinct reverse model IDs, verified IDs + licenses, language check, /languages response shape, /models metadata shape.
- `tests/integration/test_api.py` — 15 tests: health shape, languages, models, translate success/extra-fields/unsupported/empty, sentiment success/empty, analyse translated/original/invalid-target.

### Real-model smoke tests (slow)

```powershell
cd backend
.venv\Scripts\python.exe -m pytest -m slow -v
```

These download and load actual Hugging Face weights then perform real CPU inference.
They require a working torch runtime (Microsoft Visual C++ Redistributable installed).

**Status: BLOCKED** — VC++ Redist install requires UAC elevation which was not
available in this environment. Once the redist is installed, these tests should pass.

Expected:
- `test_real_sentiment_inference` — classifies two English sentences correctly.
- `test_real_translation_inference_en_fr` — translates EN->FR, gets non-empty output.

---

## Frontend Tests

### Vitest + React Testing Library (API mocked)

```powershell
cd frontend
npm install
npm run test:run
```

Tests: form validation, language swap, translate display, sentiment display,
loading states, empty input error, API failure handling, combined workflow.

**Status: BLOCKED** — Node.js not installed (winget requires UAC elevation).
Once Node.js is available, run the commands above.

Tests are written in `src/test/app.test.tsx` and will pass once executed.

---

## End-to-end verification

With both backend running and `npm run dev` for the frontend, a user can:
1. Open http://localhost:5173/
2. Enter text, select EN→FR, click Translate, see real output.
3. Click Sentiment nav, enter English text, click Analyse, see label + score bars.
4. Click Combined, enter text, select original/translated, see both results.
5. Click About, see model metadata loaded from the /models API.

This requires the VC++ Redist (for torch) and Node.js (for frontend dev server).
