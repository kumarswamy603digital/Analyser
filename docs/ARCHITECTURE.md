# Architecture

## Overview

The application follows a clean frontend/backend separation:

```
[Browser] <--> [React SPA (Vite + Tailwind)] <--> [FastAPI Backend] <--> [HuggingFace Models]
   HTTP/JSON         :5173                       :8000              CPU inference
```

## Component Diagram

```
┌──────────────────────────────────────────────────────┐
│                  React Frontend                       │
│  ┌─────────┐  ┌─────────┐  ┌────────┐  ┌────────┐  │
│  │Translate│  │Sentiment│  │Combined│  │ About  │  │
│  │  Page   │  │  Page   │  │  Page  │  │  Page  │  │
│  └────┬────┘  └────┬────┘  └───┬────┘  └───┬────┘  │
│       └────────────┴───────────┴───────────┘        │
│                         │                            │
│                  services/api.ts                     │
│               (typed fetch client)                   │
└─────────────────────────┬────────────────────────────┘
                          │ HTTP (JSON)
┌─────────────────────────┼────────────────────────────┐
│                 FastAPI Backend                       │
│  ┌───────────┐   ┌─────────────────┐   ┌──────────┐│
│  │ Routes    │──>│ Services        │──>│ ML Models││
│  │ /api/v1   │   │ translation     │   │ OPUS-MT  ││
│  │ /health   │   │ sentiment       │   │ DistilBERT││
│  └───────────┘   │ language        │   └──────────┘│
│                  └─────────────────┘               │
│  ┌────────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ Schemas    │  │ Config    │  │ Logging      │  │
│  │ (Pydantic) │  │ (env)     │  │ (structured) │  │
│  └────────────┘  └───────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Request Flow

1. User submits text + language selections in the React frontend.
2. `services/api.ts` sends a typed POST to the FastAPI backend.
3. Route handler validates via Pydantic schema (extra fields forbidden).
4. Service layer validates text (empty, length limit), resolves the model, performs inference.
5. Model uses lazy loading + per-model lock: first request downloads/loads, subsequent requests use cache.
6. Response serialized as structured JSON, returned to frontend.
7. Frontend renders result or error state.

## Model Loading Flow

1. On first use of a direction/model, `_load()` is called.
2. A thread-safe double-check lock guards initialization.
3. Heavy `import torch/transformers` happens inside the function.
4. Loaded tokenizer+model cached in a module-level dict.
5. Health endpoint reports actual load state: not loaded = not ready.
6. No model re-download on subsequent requests.
7. Preload is optional (`PRELOAD_MODELS=true` env).

## Service Responsibilities

| Service | Responsibility |
|---|---|
| `translation_service` | Validate pair, lazy-load OPUS-MT, generate, decode |
| `sentiment_service` | Validate text, load DistilBERT, classify, interpret labels |
| `language_service` | Expose registry-supported pairs to the API |

## Error Handling

All errors return a consistent `{"error": {"code", "message", "details"}}` envelope. No stack traces leak to the client. Internal errors are logged server-side with correlation IDs via structured logging.
