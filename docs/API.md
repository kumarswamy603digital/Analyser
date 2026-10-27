# API Documentation

Base URL: `http://localhost:8000`
API version prefix: `/api/v1`
Interactive docs (Swagger UI): `http://localhost:8000/docs`

All error responses use a consistent envelope:

```json
{
  "error": {
    "code": "machine_readable_code",
    "message": "Human-readable description.",
    "details": {}
  }
}
```

---

## GET /health

Returns API process availability and per-model readiness.

**Response 200:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "readiness": {
    "api_process": true,
    "translation_model_ready": false,
    "sentiment_model_ready": false
  }
}
```

Models are lazy-loaded; `*_ready` is `false` until first successful load, and never
falsely `true` after a load failure.

---

## GET /api/v1/languages

Returns supported languages and valid translation directions.

**Response 200:**
```json
{
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "fr", "name": "French"},
    {"code": "hi", "name": "Hindi"},
    {"code": "es", "name": "Spanish"}
  ],
  "directions": [
    {"source": "en", "target": "fr", "model_id": "Helsinki-NLP/opus-mt-en-fr"},
    ...
  ],
  "auto_detect_supported": false
}
```

---

## GET /api/v1/models

Returns metadata for all configured AI models.

**Response 200:**
```json
{
  "translation_models": [...],
  "sentiment_models": [{"model_id":"...", "labels":["NEGATIVE","POSITIVE"], ...}]
}
```

---

## POST /api/v1/translate

Request:
```json
{
  "text": "Hello, world",
  "source_language": "en",
  "target_language": "fr"
}
```

Response 200:
```json
{
  "source_language": "en",
  "target_language": "fr",
  "translated_text": "Bonjour le monde",
  "model_id": "Helsinki-NLP/opus-mt-en-fr",
  "processing_time_ms": 847,
  "warnings": []
}
```

Errors:
- 400: empty_input, unsupported_language_pair, invalid_language_code
- 413: input_too_long
- 500: inference_failed, model_not_ready

---

## POST /api/v1/sentiment

Request:
```json
{ "text": "I love this project!" }
```

Response 200:
```json
{
  "predicted_label": "positive",
  "scores": {"negative": 0.001, "positive": 0.999},
  "model_id": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
  "language": "en",
  "processing_time_ms": 42,
  "limitations": "English-only binary classifier...",
  "warnings": ["Scores are model confidences..."]
}
```

---

## POST /api/v1/analyse

Combined workflow.

Request:
```json
{
  "text": "I love this project!",
  "source_language": "en",
  "target_language": "fr",
  "sentiment_target": "translated"
}
```

`sentiment_target` is either `"original"` (analyse input text) or `"translated"` (analyse the output).

Response 200:
```json
{
  "translation": { ... },
  "sentiment": { ... },
  "analysed_text": "J'adore ce projet !",
  "analysed_text_origin": "translated"
}
```
