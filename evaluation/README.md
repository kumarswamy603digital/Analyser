# Evaluation

Scripts and datasets for measuring translation and sentiment quality.

## Structure

- `translation/evaluate.py` — BLEU + chrF per language pair (sacrebleu)
- `sentiment/evaluate.py` — accuracy, precision, recall, macro-F1, confusion matrix (scikit-learn)
- `translation/results.md` — actual results (generated when script is run)
- `sentiment/results.md` — actual results (generated when script is run)

## Requirements

- Backend venv with torch + transformers + sacrebleu + scikit-learn installed.
- Working Microsoft Visual C++ Redistributable (for torch DLL loading).
- Network access to Hugging Face (first model download).

## Running

```bash
cd backend
.venv\Scripts\activate
python ../evaluation/translation/evaluate.py --all
python ../evaluation/sentiment/evaluate.py
```

Results are written to `results.md` in each subdirectory.

## Important Notes

- Test sets are small (2-15 samples per pair) — results are INDICATIVE only.
- BLEU/chrF do not fully capture translation quality; manual inspection is essential.
- Sentiment metrics are for English-only binary model; do not generalize to other languages/domains.
- Results are only real if the models actually ran. If evaluation cannot run, do NOT fabricate scores.
