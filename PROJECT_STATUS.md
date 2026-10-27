# PROJECT_STATUS.md

Living status log for **Our Own Translator & Sentiment Analyser**.

## Latest update - coding-complete pass
All source code, configuration, environment files, feature hooks, components,
pages, startup scripts and docs required to run the application end-to-end are
now written. What is still pending is strictly *runtime* verification (needs
Node.js and Microsoft Visual C++ Redistributable installed by an admin):
- `pip install` in the backend venv has completed, so the backend starts and
  serves metadata endpoints. `pytest -q` currently reports **37 passed,
  2 deselected**.
- Real model inference (smoke tests, evaluation scripts, live translate /
  sentiment calls) still requires the VC++ runtime to be installed so that
  `torch` can load.
- `npm install`, `npm run dev` and `npm run test:run` for the frontend require
  Node.js to be installed.

New / updated files in this pass:
- `frontend/src/vite-env.d.ts`
- `frontend/src/features/translator/useTranslator.ts`
- `frontend/src/features/sentiment/useSentiment.ts`
- `frontend/src/features/combined/useCombined.ts`
- `frontend/src/pages/{Translator,Sentiment,Combined}.tsx` rewritten to consume
  feature hooks; field names aligned with actual backend response schema
- `frontend/src/components/{Card,Button,ScoreBar}.tsx` (title prop, ghost
  variant, scores-map ScoreBar)
- `frontend/src/index.css` (utility classes for textarea/select/badge/btn)
- `frontend/src/test/app.test.tsx` (label selector fix)
- `backend/.env` and `frontend/.env.local` (working defaults, not just examples)
- `scripts/{setup-backend,start-backend,setup-frontend,start-frontend,run-tests}.ps1`

## Environment (verified at start)
- OS: Windows 25H2, shell PowerShell.
- Python: 3.14.7 (pip 26.2.1). torch 2.14.1+cpu, transformers 5.21.0 installed in venv.
- Node.js / npm: NOT installed. winget attempt auto-cancelled (UAC 1602).
- Microsoft Visual C++ Redistributable: NOT installed. winget attempt auto-cancelled (UAC 1602).
- Docker: NOT installed.
- Git: 2.55.0.
- Network to huggingface.co: OK (HTTP 200).

## Model registry (all verified live on Hugging Face)
- en->hi Helsinki-NLP/opus-mt-en-hi ; hi->en Helsinki-NLP/opus-mt-hi-en
- en->fr Helsinki-NLP/opus-mt-en-fr ; fr->en Helsinki-NLP/opus-mt-fr-en
- en->es Helsinki-NLP/opus-mt-en-es ; es->en Helsinki-NLP/opus-mt-es-en
- sentiment distilbert/distilbert-base-uncased-finetuned-sst-2-english (POS/NEG)
- All licenses: Apache-2.0 (verified via HF tags).

## Commands executed
- `git init`, mkdir project tree
- `python -m venv .venv`, `pip install -r requirements.txt` (SUCCESS, all packages installed)
- `python -m pytest -q` from backend/ (fast tests: **37 passed, 2 deselected**)
- `winget install Microsoft.VCRedist.2015+.x64` — FAILED (exit 1602, UAC cancelled)
- `winget install OpenJS.NodeJS.LTS` — FAILED (exit 1602, UAC cancelled)
- `python -c "from app.main import app"` — SUCCESS (FastAPI app imports without torch)

## Test results
- Backend fast tests (37): ALL PASS. Verified validation, error handling, schemas, routing.
- Backend real-model smoke (2): BLOCKED — requires VC++ Redistributable for torch DLL.
- Frontend tests (Vitest + RTL): BLOCKED — requires Node.js to run npm/vitest.
- End-to-end: BLOCKED — requires both Node.js and VC++ redist.

## Stage log

### Stage 0 - Scaffolding  [DONE]
- git repo, .gitignore, .env.example, LICENSE, PROJECT_STATUS.md, directory tree.

### Stage 1 - Backend skeleton  [DONE]
- requirements.txt (pinned), config.py, logging.py, exceptions.py, schemas, main.py, /health.
- Verified: app imports without error.

### Stage 2 - Translation engine  [DONE]
- ml/model_registry.py (6 verified pairs), services/translation_service.py (lazy+lock+CPU).
- Routes: POST /api/v1/translate, GET /api/v1/languages.
- Verified via unit + integration tests (mocked).

### Stage 3 - Sentiment engine  [DONE]
- services/sentiment_service.py (lazy+lock+inference_mode+softmax+label mapping).
- Routes: POST /api/v1/sentiment, GET /api/v1/models.
- Verified via unit tests (_interpret, mocked analyze) + integration.

### Stage 4 - Combined analysis  [DONE]
- POST /api/v1/analyse: translates then classifies chosen text (original/translated).
- Includes honest English-only warning for non-EN original analysis.
- Verified via integration tests (mocked).

### Stage 5 - Backend tests  [DONE - FAST SUITE]
- 37 pytest tests passing (unit + integration, all inference mocked).
- 2 slow smoke tests written but cannot execute (torch DLL requires VC++ redist).

### Stage 6 - Frontend  [CODE COMPLETE, RUN PENDING]
- All source written: package.json, tsconfig, vite/tailwind/postcss configs.
- 4 pages (Translator, Sentiment, Combined, About) with full UI.
- Reusable components: Button, Card, Alert, ScoreBar.
- hooks/useTheme, hooks/useLanguages. Dark/light mode. Accessible labels.
- Cannot run npm install/dev/build/test without Node.js.

### Stage 7 - Frontend integration  [CODE COMPLETE]
- services/api.ts: typed fetch client, error handling, configurable base URL.
- .env.example with VITE_API_BASE_URL. All pages call real endpoints via API client.

### Stage 8 - Frontend tests  [CODE COMPLETE, RUN PENDING]
- src/test/app.test.tsx: 5 Vitest+RTL tests (validation, swap, display, sentiment).
- Cannot execute without Node.js.

### Stage 9 - Evaluation  [SCRIPTS COMPLETE, EXECUTION PENDING]
- evaluation/translation/evaluate.py: BLEU + chrF per pair (sacrebleu).
- evaluation/sentiment/evaluate.py: accuracy, precision, recall, macro-F1, confusion matrix.
- Cannot execute without torch (requires VC++ redist).

### Stage 10 - Docs / Docker / Deployment  [DONE]
- README.md, docs/ARCHITECTURE.md, API.md, MODEL_CARD.md, TESTING.md, DEPLOYMENT.md,
  INTERNSHIP_REPORT.md (with PLACEHOLDERs), DEMO_SCRIPT.md, evaluation/README.md.
- Dockerfile.backend, Dockerfile.frontend, docker-compose.yml (NOT verified - Docker absent).

## Known limitations
1. VC++ Redistributable cannot be installed non-interactively; blocks torch import and all
   real inference (smoke tests, evaluation scripts, live API translate/sentiment).
2. Node.js cannot be installed non-interactively; blocks frontend npm install, dev server,
   build, and Vitest execution.
3. Docker absent; deployment is documented but unverified.
4. Sentiment is 2-class English-only; no neutral, no multilingual.
5. No automatic source-language detection in v1.

## Unresolved action required from user
To complete the final quality gate, install these manually (elevated PowerShell):
1. **VC++ Redistributable x64**: Download and run https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Then verify: `cd backend; .venv\Scripts\python.exe -c "import torch; print(torch.__version__)"`
   - Then run: `python -m pytest -m slow` (real-model smoke)
   - Then run: evaluation scripts
2. **Node.js LTS**: Download from https://nodejs.org or run `winget install OpenJS.NodeJS.LTS` from
   an Administrator PowerShell.
   - Then: `cd frontend; npm install; npm run test:run; npm run build`
3. Start backend and frontend, verify end-to-end in browser.

## Next steps
- After user installs VC++ redist + Node.js, execute real tests and fill evaluation results.md.
- Update docs/INTERNSHIP_REPORT.md section 13 with real numbers.
- Execute final quality gate checklist.
