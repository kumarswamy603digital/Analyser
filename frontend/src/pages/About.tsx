import { useEffect, useState } from "react";
import Card from "../components/Card";
import Alert from "../components/Alert";
import { getModels } from "../services/api";
import type { ModelsResponse } from "../types/api";

export default function About() {
  const [models, setModels] = useState<ModelsResponse | null>(null);

  useEffect(() => {
    getModels().then(setModels).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">About &amp; Model Information</h2>

      <Alert type="warning">
        Predictions may be inaccurate. This application uses pretrained AI models for
        translation and sentiment classification. Results should not be treated as
        authoritative or used in critical decisions without human review.
      </Alert>

      <Card>
        <h3 className="font-semibold mb-2">Translation Models</h3>
        <p className="text-sm mb-3">
          Helsinki-NLP OPUS-MT models (Apache-2.0) running locally on CPU. Each language
          direction uses a dedicated model (e.g. EN→FR and FR→EN are separate).
        </p>
        {models?.translation_models && (
          <ul className="text-sm space-y-1 list-disc pl-5">
            {models.translation_models.map((m) => (
              <li key={m.model_id}>
                <code>{m.model_id}</code> ({m.supported_languages.join(" → ")})
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card>
        <h3 className="font-semibold mb-2">Sentiment Model</h3>
        <p className="text-sm mb-3">
          DistilBERT fine-tuned on SST-2 (Apache-2.0) — binary English-only (positive/negative).
        </p>
        {models?.sentiment_models?.[0] && (
          <div className="text-sm">
            <p>Model: <code>{models.sentiment_models[0].model_id}</code></p>
            <p>Labels: {models.sentiment_models[0].labels?.join(", ")}</p>
            <p className="mt-2 text-slate-500">{models.sentiment_models[0].limitations}</p>
          </div>
        )}
      </Card>

      <Card>
        <h3 className="font-semibold mb-2">Project Details</h3>
        <ul className="text-sm space-y-1 list-disc pl-5">
          <li>AI Internship Project — Our Own Translator &amp; Sentiment Analyser</li>
          <li>Stack: FastAPI (Python) + React/TypeScript + Vite + Tailwind CSS</li>
          <li>No paid API keys; all inference is local via Hugging Face Transformers.</li>
          <li>Input text is not permanently stored. Optional history is local-only.</li>
        </ul>
      </Card>
    </div>
  );
}
