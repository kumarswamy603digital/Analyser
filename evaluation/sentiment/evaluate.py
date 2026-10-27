"""
Sentiment evaluation: accuracy, precision, recall, macro F1, confusion matrix.

Requires: scikit-learn, working torch runtime.
Usage:
    cd backend
    python ../evaluation/sentiment/evaluate.py

This uses a small labeled test set defined inline. In a production project you'd use
a held-out split of SST-2 or a larger independent corpus.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

# Small labeled dataset (text, gold_label). Positive/negative binary.
# Intentionally separate from training data (SST-2 train split).
# These examples are human-labeled for this evaluation only.
TEST_SET: list[tuple[str, str]] = [
    ("I absolutely loved this movie, it was fantastic!", "positive"),
    ("The food was delicious and the service was excellent.", "positive"),
    ("What a wonderful and inspiring experience!", "positive"),
    ("I'm so happy with the results.", "positive"),
    ("Great product, highly recommend it to everyone.", "positive"),
    ("This is terrible and a complete waste of time.", "negative"),
    ("I hated every minute of it.", "negative"),
    ("The worst experience I have ever had.", "negative"),
    ("Absolutely dreadful, do not buy this.", "negative"),
    ("I'm very disappointed with the poor quality.", "negative"),
]


def main():
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        classification_report,
    )
    from app.services.sentiment_service import analyze

    labels = []
    preds = []
    for text, gold in TEST_SET:
        try:
            result = analyze(text)
            pred = result.predicted_label
        except Exception as e:
            print(f"ERROR: {text[:40]}... -> {e}")
            pred = "error"
        labels.append(gold)
        preds.append(pred)

    # Filter out any errors
    valid = [(l, p) for l, p in zip(labels, preds) if p != "error"]
    y_true = [l for l, p in valid]
    y_pred = [p for l, p in valid]

    if len(y_true) == 0:
        print("No valid predictions. Cannot compute metrics.")
        return

    out = "\n## Sentiment Evaluation Results\n\n"
    out += f"**Dataset:** {len(TEST_SET)} samples (10 labeled sentences)\n\n"
    out += f"**Valid predictions:** {len(y_true)}\n\n"
    out += "| Metric | Value |\n|---|---|\n"
    out += f"| Accuracy | {accuracy_score(y_true, y_pred):.3f} |\n"
    out += f"| Precision (macro) | {precision_score(y_true, y_pred, average='macro', zero_division=0):.3f} |\n"
    out += f"| Recall (macro) | {recall_score(y_true, y_pred, average='macro', zero_division=0):.3f} |\n"
    out += f"| F1 (macro) | {f1_score(y_true, y_pred, average='macro', zero_division=0):.3f} |\n"

    out += "\n### Confusion Matrix\n\n"
    cm = confusion_matrix(y_true, y_pred, labels=["negative", "positive"])
    out += f"```\n            Pred: Neg  Pos\n  True: Neg    {cm[0][0]:3d}   {cm[0][1]:3d}\n"
    out += f"  True: Pos    {cm[1][0]:3d}   {cm[1][1]:3d}\n```\n"

    out += "\n### Classification Report\n\n```\n"
    out += classification_report(y_true, y_pred, labels=["negative", "positive"], zero_division=0)
    out += "```\n"

    out += "\n### Limitations\n"
    out += "- Small dataset (10 samples) — results are indicative, not definitive.\n"
    out += "- Sentiment model is English-only (SST-2 trained); domain coverage is limited.\n"
    out += "- Does not generalize to all languages, domains, or populations.\n"
    print(out)

    results_path = os.path.join(os.path.dirname(__file__), "results.md")
    with open(results_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Results written to {results_path}")


if __name__ == "__main__":
    main()
