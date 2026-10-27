# Demonstration Script (5-7 minutes)

## 1. Introduction to the Problem (30s)
- "This is an AI-powered web application that performs neural machine translation and
  sentiment analysis. Students and professionals need a free, self-hosted tool to
  translate text and analyze its emotional tone without paid APIs."

## 2. Architecture Overview (60s)
- Show docs/ARCHITECTURE.md diagram or explain briefly:
  "React frontend calls a FastAPI backend. The backend lazy-loads Hugging Face
  transformer models on first request and caches them in memory. All inference runs
  locally on CPU. No API keys needed."

## 3. Live Demo — Translation (90s)
- Start backend: `uvicorn app.main:app --reload`
- Open frontend http://localhost:5173/
- Enter "Hello, how are you today?", select EN→FR, click Translate.
- Show real output from OPUS-MT model.
- Note model ID and processing time displayed in the footer.
- Try EN→HI to show Hindi support.

## 4. Live Demo — Sentiment (60s)
- Navigate to Sentiment Analyser.
- Enter "I absolutely loved this movie, it was fantastic!"
- Click Analyse. Show POSITIVE label and actual score bars.
- Try a negative sentence.
- Point to the limitations warning: English-only, binary, scores are model confidence.

## 5. Live Demo — Combined Workflow (60s)
- Navigate to Combined Analysis.
- Enter a sentence, translate EN→FR, choose "translated" for sentiment.
- Show both results side by side with clear labelling.
- Switch to "original" and note the English-only warning for non-EN original.

## 6. API Documentation (30s)
- Open http://localhost:8000/docs (Swagger UI).
- Show endpoint list, example request/response schemas.

## 7. Model Selection (30s)
- Navigate to About page.
- Show model IDs, licenses (Apache-2.0), supported languages, limitations.

## 8. Evaluation Results (30s)
- Open evaluation/translation/results.md and evaluation/sentiment/results.md.
- Present actual BLEU/chrF/F1 numbers.
- Note: small dataset, metrics don't fully capture quality.

## 9. Limitations and Future Scope (30s)
- No neutral sentiment, English-only sentiment, no auto-detect, small eval set.
- Future: multilingual sentiment, more languages, ONNX optimization, batch CSV.

## 10. Tests and Code Quality (optional 30s)
- Mention 37 backend tests passing (pytest), frontend test suite (Vitest+RTL).
- Show error envelope, input validation, and thread-safe model loading.

---

**Total: ~5-7 minutes**
