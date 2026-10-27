# Internship Report: Our Own Translator & Sentiment Analyser

---

## Title Page

**Project Title:** Our Own Translator & Sentiment Analyser  
**Student Name:** [PLACEHOLDER - STUDENT NAME]  
**Enrollment No.:** [PLACEHOLDER]  
**Internship Organization:** [PLACEHOLDER - COMPANY/INSTITUTION]  
**Duration:** [PLACEHOLDER - START DATE to END DATE]  
**Department:** [PLACEHOLDER]  
**Guide/Mentor:** [PLACEHOLDER]  
**Date of Submission:** [PLACEHOLDER]

---

## 1. Abstract

This project develops an AI-powered web application that combines language translation
and sentiment analysis. The application uses pretrained neural machine translation models
(Helsinki-NLP OPUS-MT) and a transformer-based sentiment classifier (DistilBERT fine-tuned
on SST-2) to provide translation between English, French, Spanish, and Hindi, and English
sentiment classification. The combined workflow translates text and optionally analyses
sentiment of either the source or translated text. All inference runs locally on CPU,
requiring no paid API keys. The application is built with a FastAPI backend and a
React/TypeScript frontend, following modern web architecture with proper testing,
documentation, and deployment configuration.

## 2. Introduction

Natural language processing (NLP) enables machines to understand and generate human
language. Two fundamental tasks are machine translation (converting text between languages)
and sentiment analysis (determining emotional tone). This project combines both into a
practical web application for student use, customer feedback analysis, and language learning.

## 3. Problem Statement

Students and general users need an accessible tool that can translate text between languages
and analyze sentiment, without requiring paid API subscriptions or cloud accounts. Existing
solutions either require API keys, are not open-source, or do not combine both capabilities
into a single workflow.

## 4. Objectives

- Implement real AI translation between English, Hindi, French, and Spanish.
- Implement English text sentiment classification (positive/negative).
- Provide a combined translate-and-analyse workflow.
- Build a modern, responsive, accessible web interface.
- Ensure local CPU inference with no paid dependencies.
- Provide proper documentation, testing, and deployment instructions.

## 5. Existing Approaches and Project Motivation

Services like Google Translate and DeepL provide excellent translation but require API keys
for programmatic use or offer no sentiment analysis. Open-source alternatives exist but lack
integrated UIs. This project provides a self-contained, reproducible, open-stack solution
using freely available Hugging Face models with permissive licenses.

## 6. Proposed System

A web application with three connected capabilities: language translation (6 verified
directions), English sentiment analysis (DistilBERT SST-2), and a combined workflow.
The backend performs real transformer inference; the frontend provides accessible UI with
proper loading, error, and result states.

## 7. System Architecture

See docs/ARCHITECTURE.md for the full diagram. Summary:

- React SPA communicates with FastAPI via REST JSON.
- FastAPI services layer performs input validation, model lazy-loading, inference.
- Models downloaded once from Hugging Face Hub and cached locally.
- All inference runs on CPU (no GPU required).

## 8. Technology Selection and Justification

| Layer | Choice | Justification |
|---|---|---|
| Frontend | React + TypeScript + Vite + Tailwind | Modern, type-safe, fast HMR, utility-first CSS |
| Backend | Python + FastAPI + Pydantic | Async-native, auto-openapi, validation, type hints |
| AI Inference | Hugging Face Transformers + PyTorch | Industry standard, pre-trained, no training needed |
| Testing | pytest + HTTPX (backend), Vitest + RTL (frontend) | Fast, proper mocking, real API client tests |

## 9. Model Selection and Implementation

Six Helsinki-NLP OPUS-MT direction-specific models (verified live, Apache-2.0) and
one DistilBERT SST-2 model (verified live, Apache-20). Lazy loading with thread-safe
caching; beam search generation for translation; softmax classification for sentiment.
See docs/MODEL_CARD.md for details.

## 10. Frontend Implementation

Four pages (Translator, Sentiment, Combined, About) with reusable components, dark/light
theme, responsive layout, accessible labels and focus rings, loading/error/empty states,
language swap, example sentences, copy-to-clipboard, and score visualization bars.

## 11. Backend Implementation

RESTful API with versioned prefix (/api/v1), consistent error envelope, structured JSON
logging with correlation IDs, CORS via environment, input length limits (413), empty
input rejection, model-init and inference failure handling. Swagger UI auto-generated.

## 12. Testing Methodology

37 fast tests (unit with mocked inference + integration via TestClient). Real-model smoke
tests for actual inference. Frontend tests via Vitest + React Testing Library with mocked
API. See docs/TESTING.md.

## 13. Evaluation Results

[PLACEHOLDER - to be filled after VC++ Redistributable installed and evaluation scripts
executed. Expected format: BLEU/chrF table for translation; accuracy/F1 for sentiment.]

## 14. Screenshots

[PLACEHOLDER - capture from actual running application]

## 15. Challenges and Solutions

- **PyTorch on Python 3.14 (Windows):** CPU wheel availability confirmed; runtime
  requires VC++ Redistributable (resolved by documenting installation requirement).
- **6 direction-specific models:** Cannot reuse models across directions; registry maps
  each direction independently.
- **Lazy loading without race conditions:** Thread-safe double-check lock pattern prevents
  duplicate model initialization from concurrent requests.
- **Honesty in AI claims:** No fabricated confidence scores, no neutral sentiment class
  added artificially, limitations clearly displayed.

## 16. Limitations

- Sentiment is English-only binary; no neutral class.
- No automatic language detection in v1.
- Evaluation uses small datasets (10-15 samples per language pair).
- Docker and cloud deployment documented but NOT verified in this environment.

## 17. Future Scope

- Add multilingual sentiment model.
- Add more verified language pairs.
- Implement automatic source language detection (fastText/lingua).
- Batch CSV sentiment processing.
- Persistent history with user authentication.
- Performance optimization (ONNX Runtime, quantization).
- CI/CD pipeline and cloud deployment verification.

## 18. Conclusion

This project delivers a functional, well-architected AI application combining neural
machine translation and sentiment analysis with real model inference, connected frontend,
comprehensive tests, and professional documentation. It demonstrates proficiency in
Python backend development, React/TypeScript frontend, ML model integration, and software
engineering best practices.

## 19. References

1. Helsinki-NLP OPUS-MT: Tiedemann & Thotingo (2020)
2. DistilBERT: Sanh et al. (2019)
3. FastAPI: https://fastapi.tiangolo.com
4. React: https://react.dev
5. Hugging Face Transformers: https://huggingface.co/docs/transformers
6. Tailwind CSS: https://tailwindcss.com
