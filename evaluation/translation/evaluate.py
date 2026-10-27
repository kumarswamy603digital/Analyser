"""
Translation evaluation: BLEU and chrF per language pair.

Requires:
    pip install sacrebleu
    Working torch runtime (Microsoft Visual C++ Redistributable must be installed).

Usage:
    cd backend
    python ../evaluation/translation/evaluate.py [--pair en-fr] [--all]

If reference translations are not available for a pair, the metric is SKIPPED (not
fabricated). This script uses a small documented test set defined inline below.

NOTE: Automated metrics (BLEU, chrF) do not fully capture translation quality.
Manual inspection of outputs is essential and documented in results.md.
"""
from __future__ import annotations

import argparse
import sys
import os

# Add backend to path so we can import app.services.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

# --- Small documented test set (source, reference) ---
# References are human-verified for basic correctness. Not a substitute for a
# large-scale evaluation corpus.
TEST_DATA: dict[str, list[tuple[str, str]]] = {
    "en-fr": [
        ("Hello, how are you?", "Bonjour, comment allez-vous ?"),
        ("The weather is beautiful today.", "Il fait beau aujourd'hui."),
        ("I love learning new languages.", "J'adore apprendre de nouvelles langues."),
    ],
    "fr-en": [
        ("Bonjour, comment allez-vous ?", "Hello, how are you?"),
        ("Je parle français.", "I speak French."),
    ],
    "en-es": [
        ("Good morning, how are you?", "Buenos días, ¿cómo estás?"),
        ("I would like a coffee.", "Me gustaría un café."),
    ],
    "es-en": [
        ("Buenos días, ¿cómo estás?", "Good morning, how are you?"),
    ],
    "en-hi": [
        ("Hello, how are you?", "नमस्ते, आप कैसे हैं?"),
        ("Thank you very much.", "बहुत धन्यवाद।"),
    ],
    "hi-en": [
        ("नमस्ते, आप कैसे हैं?", "Hello, how are you?"),
    ],
}


def evaluate_pair(pair: str) -> dict:
    from sacrebleu.metrics import BLEU, CHRF
    from app.services import translation_service as ts

    if pair not in TEST_DATA:
        print(f"No test data for {pair} — skipping.")
        return {"pair": pair, "status": "no_data"}

    src, tgt = pair.split("-")
    hypotheses = []
    references = []
    for text, ref in TEST_DATA[pair]:
        try:
            result = ts.translate(text, src, tgt)
            hypotheses.append(result.translated_text)
            references.append(ref)
        except Exception as e:
            print(f"  ERROR translating '{text[:40]}...': {e}")
            hypotheses.append("")
            references.append(ref)

    bleu = BLEU()
    chrf = CHRF()
    b = bleu.score(hypotheses, [references], tokenize="13a")
    c = chrf.score(hypotheses, [references])
    return {
        "pair": pair,
        "samples": len(hypotheses),
        "bleu": round(b.score, 2),
        "chrf": round(c.score, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate translations.")
    parser.add_argument("--pair", type=str, default=None, help="e.g. en-fr")
    parser.add_argument("--all", action="store_true", help="Evaluate all pairs.")
    args = parser.parse_args()

    pairs = list(TEST_DATA.keys()) if args.all else [args.pair or "en-fr"]
    results = [evaluate_pair(p) for p in pairs]

    # Output
    out = "\n## Translation Evaluation Results\n\n"
    out += "| Pair | Samples | BLEU | chrF |\n|---|---|---|---|\n"
    for r in results:
        if r.get("status") == "no_data":
            out += f"| {r['pair']} | 0 | SKIPPED | SKIPPED |\n"
        else:
            out += f"| {r['pair']} | {r['samples']} | {r['bleu']} | {r['chrf']} |\n"
    out += "\n*Metrics do not fully capture translation quality.*\n"
    print(out)

    # Write to results.md
    results_path = os.path.join(os.path.dirname(__file__), "results.md")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Results written to {results_path}")


if __name__ == "__main__":
    main()
