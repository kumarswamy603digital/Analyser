# Our Own Translator & Sentiment Analyser

AI-powered web application: neural machine translation + English sentiment classification
+ combined analysis workflow. Real Hugging Face model inference on CPU. No paid API keys.

## Features

- **Translation**: English, French, Spanish, Hindi (6 verified directions via OPUS-MT)
- **Sentiment Analysis**: English binary classification (positive/negative via DistilBERT SST-2)
- **Combined Workflow**: Translate, then analyse sentiment of original or translated text
- **Responsive UI**: Dark/light theme, accessible, mobile-friendly
- **API Documentation**: Auto-generated Swagger UI at `/docs`
- **Properly Tested**: 37 backend tests (pytest), frontend tests (Vitest + RTL)
- **Docker Ready**: Compose file for containerized deployment

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript 5, Vite 5, Tailwind CSS 3, Vitest, React Testing Library |
| Backend | Python 3.14, FastAPI, Pydantic v2, Uvicorn, Hugging Face Transformers, PyTorch (CPU) |
| AI Models | Helsinki-NLP OPUS-MT (6 directions), DistilBERT SST-2 |
| DevOps | Git, Docker, GitHub-ready structure |

## Repository Structure

```
project-root/
  frontend/          React SPA (src/pages, components, hooks, services, types, tests)
  backend/           FastAPI (app/, tests/, requirements.txt)
  evaluation/        Translation (BLEU/chrF) + Sentiment (accuracy/F1) scripts
  docs/              Architecture, API, Model Card, Testing, Deployment, Internship Report
  scripts/           Helper scripts
  docker-compose.yml Frontend + backend container orchestration
  Dockerfile.backend Python backend container
  Dockerfile.frontend Node build + nginx serve
  PROJECT_STATUS.md  Stage-by-stage development log
  .env.example       Environment template
```

## Prerequisites

- **Python 3.12+** (tested with 3.14.7)
- **Microsoft Visual C++ Redistributable x64** (for PyTorch DLL loading)
  Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
- **Node.js 18+** (tested with 24.x LTS)
- Network access to huggingface.co (first model download, ~300 MB total)

## Installation & Running

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env          # or copy on Windows
uvicorn app.main:app --reload
```

API: http://localhost:8000 | Swagger docs: http://localhost:8000/docs | Health: /health

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

UI: http://localhost:5173

### Docker (optional, requires Docker installed)

```bash
docker compose up --build
```

Frontend at localhost:5173, backend at localhost:8000.

## Testing

### Backend (fast, no model download needed)

```bash
cd backend
.venv\Scripts\python.exe -m pytest
```

### Backend (real-model smoke tests)

```bash
.venv\Scripts\python.exe -m pytest -m slow
```

### Frontend

```bash
cd frontend
npm run test:run
```

## AI Models

| Task | Model | License |
|---|---|---|
| EN→FR translation | Helsinki-NLP/opus-mt-en-fr | Apache-2.0 |
| FR→EN translation | Helsinki-NLP/opus-mt-fr-en | Apache-2.0 |
| EN→ES translation | Helsinki-NLP/opus-mt-en-es | Apache-2.0 |
| ES→EN translation | Helsinki-NLP/opus-mt-es-en | Apache-2.0 |
| EN→HI translation | Helsinki-NLP/opus-mt-en-hi | Apache-2.0 |
| HI→EN translation | Helsinki-NLP/opus-mt-hi-en | Apache-2.0 |
| Sentiment (EN) | distilbert/distilbert-base-uncased-finetuned-sst-2-english | Apache-2.0 |

See `docs/MODEL_CARD.md` for full details.

## Evaluation

Run evaluation scripts (requires working torch runtime):

```bash
cd backend
.venv\Scripts\python.exe ../evaluation/translation/evaluate.py --all
.venv\Scripts\python.exe ../evaluation/sentiment/evaluate.py
```

Results written to `evaluation/translation/results.md` and `evaluation/sentiment/results.md`.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /health | API + model readiness |
| GET | /api/v1/languages | Supported languages + directions |
| GET | /api/v1/models | Model metadata |
| POST | /api/v1/translate | Translate text |
| POST | /api/v1/sentiment | Classify sentiment |
| POST | /api/v1/analyse | Combined: translate + sentiment |

Full details: docs/API.md

## Known Limitations

- Sentiment: English-only, binary (positive/negative only, no neutral).
- No automatic source-language detection; user must select explicitly.
- Translation and sentiment evaluation use small datasets — indicative, not definitive.
- Docker/cloud deployment documented but NOT verified in the development environment.
- First model call downloads weights (~300 MB total); cached locally.

## Future Improvements

- Multilingual sentiment model
- Automatic language detection (lingua/fastText)
- Additional verified OPUS-MT pairs
- Batch CSV sentiment analysis
- ONNX Runtime quantization for faster inference
- Persistent analysis history + export
- Cloud deployment verification

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Model Card](docs/MODEL_CARD.md)
- [Testing](docs/TESTING.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Internship Report](docs/INTERNSHIP_REPORT.md)
- [Demo Script](docs/DEMO_SCRIPT.md)
- [Project Status](PROJECT_STATUS.md)

## License

MIT (application code). Model weights carry their own licenses — see docs/MODEL_CARD.md.
