# Model Card

## Translation Models

| Property | Value |
|---|---|
| Family | Helsinki-NLP OPUS-MT |
| Architecture | Marian NMT (encoder-decoder, sentencepiece BPE) |
| License | Apache-2.0 (verified via HF Hub tag `license:apache-2.0`) |
| Task | Neural machine translation |
| Intended use | General-purpose sentence-level translation |

### Supported Directions

Each direction uses its own dedicated model. Reversing direction does NOT reuse the same weights.

| Direction | Model ID |
|---|---|
| English → Hindi | `Helsinki-NLP/opus-mt-en-hi` |
| Hindi → English | `Helsinki-NLP/opus-mt-hi-en` |
| English → French | `Helsinki-NLP/opus-mt-en-fr` |
| French → English | `Helsinki-NLP/opus-mt-fr-en` |
| English → Spanish | `Helsinki-NLP/opus-mt-en-es` |
| Spanish → English | `Helsinki-NLP/opus-mt-es-en` |

### Inference Method

- Loaded via `AutoTokenizer.from_pretrained()` + `AutoModelForSeq2SeqLM.from_pretrained()`
- CPU by default; GPU optional
- Generation: beam search (`num_beams=4`), `no_repeat_ngram_size=3`
- Model cached per direction in-process; lazy-loaded on first request

### Limitations

- Trained on general web parallel corpora; domain-specific text may be mistranslated
- Long inputs truncated to 512 tokens
- Not suitable for legal/medical translation without human review

---

## Sentiment Model

| Property | Value |
|---|---|
| Model ID | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` |
| Architecture | DistilBERT (6-layer transformer encoder) |
| License | Apache-2.0 (verified via HF Hub tag) |
| Task | Text classification (binary sentiment) |
| Labels | NEGATIVE (0), POSITIVE (1) |
| Training | Fine-tuned on SST-2 binary split |
| Intended use | English text sentiment classification |

### Inference Method

- Loaded via `AutoTokenizer` + `AutoModelForSequenceClassification`
- `torch.inference_mode()` (no gradient tracking)
- Softmax over logits yields scores for each class
- Predicted label = argmax of probability distribution
- Truncation: max 512 subword tokens (right-truncated)

### Limitations

- **Binary only** — no neutral class
- **English only** — does NOT reliably handle Hindi, French, Spanish, or other languages
- Scores are model confidences, not guaranteed real-world probabilities
- May fail on sarcasm, negation-heavy, mixed-sentiment, or out-of-domain text
- Small evaluation dataset used (10 samples); production use requires larger benchmarks
- No explanation capability (just classification)
- Does not analyze emotion types beyond positive/negative
