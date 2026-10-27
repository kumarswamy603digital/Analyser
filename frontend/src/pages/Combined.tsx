import { useLanguages } from "../hooks/useLanguages";
import { useCombined } from "../features/combined/useCombined";
import Card from "../components/Card";
import Button from "../components/Button";
import Alert from "../components/Alert";
import ScoreBar from "../components/ScoreBar";
import type { SentimentTarget } from "../types/api";

const MAX_CHARS = 1000;

export default function Combined() {
  const { data: langData } = useLanguages();
  const {
    source, setSource,
    target, setTarget,
    sentTarget, setSentTarget,
    input, setInput,
    result, loading, error,
    run, clear,
  } = useCombined();

  const languages = langData?.languages ?? [];

  return (
    <div className="mx-auto w-full max-w-3xl space-y-4">
      <h1 className="text-2xl font-bold">Combined Workflow</h1>
      <p className="text-sm text-slate-600 dark:text-slate-300">
        Translate text into English, then run sentiment analysis on the original
        or the translated version.
      </p>

      <Card>
        <div className="flex flex-wrap items-center gap-3 text-sm">
          <label className="label !mb-0">
            From
            <select
              aria-label="Source language"
              className="select ml-2"
              value={source}
              onChange={(e) => setSource(e.target.value)}
            >
              {languages.map((l) => <option key={l.code} value={l.code}>{l.name}</option>)}
            </select>
          </label>
          <label className="label !mb-0">
            To
            <select
              aria-label="Target language"
              className="select ml-2"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            >
              {languages.map((l) => <option key={l.code} value={l.code}>{l.name}</option>)}
            </select>
          </label>
          <label className="label !mb-0">
            Analyse
            <select
              aria-label="Sentiment target"
              className="select ml-2"
              value={sentTarget}
              onChange={(e) => setSentTarget(e.target.value as SentimentTarget)}
            >
              <option value="translated">Translated text</option>
              <option value="original">Original text</option>
            </select>
          </label>
        </div>

        <div className="mt-4">
          <label className="label" htmlFor="combined-text">Input text</label>
          <textarea
            id="combined-text"
            aria-label="Combined text input"
            className="textarea min-h-32"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            maxLength={MAX_CHARS}
            placeholder="Enter text to translate and analyse..."
          />
          <div className="mt-1 text-xs text-slate-500">
            {input.length} / {MAX_CHARS} characters
          </div>
        </div>

        <div className="mt-4 flex gap-2">
          <Button onClick={run} disabled={loading} variant="primary">
            {loading ? "Running…" : "Run Analysis"}
          </Button>
          <Button onClick={clear} disabled={loading} variant="ghost">Clear</Button>
        </div>

        {error && <div className="mt-4"><Alert type="error">{error}</Alert></div>}
      </Card>

      {result && (
        <>
          <Card title={`Translation (${result.translation.source_language} → ${result.translation.target_language})`}>
            <pre className="whitespace-pre-wrap break-words rounded-md bg-slate-100 p-3 font-mono text-sm dark:bg-slate-800">
              {result.translation.translated_text}
            </pre>
            <p className="mt-2 text-xs text-slate-500">
              Model <code>{result.translation.model_id}</code> • {result.translation.processing_time_ms} ms
            </p>
            {result.translation.warnings.length > 0 && (
              <div className="mt-3 space-y-2">
                {result.translation.warnings.map((w, i) => <Alert key={i} type="warning">{w}</Alert>)}
              </div>
            )}
          </Card>

          <Card title={`Sentiment (analysed: ${result.analysed_text_origin} text)`}>
            <p className="mb-2 text-xs text-slate-500">
              Analysed text: “{result.analysed_text}”
            </p>
            <div className="flex items-center justify-between gap-4">
              <div>
                <span className="text-sm text-slate-500">Predicted label</span>
                <div className="mt-1">
                  <span className={"badge badge-lg " +
                    (result.sentiment.predicted_label === "positive" ? "badge-success" : "badge-error")}>
                    {result.sentiment.predicted_label.toUpperCase()}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold">
                  {Math.max(...Object.values(result.sentiment.scores)).toFixed(2)}
                </div>
                <div className="text-xs text-slate-500">top confidence</div>
              </div>
            </div>

            <div className="mt-5">
              <ScoreBar scores={result.sentiment.scores} />
            </div>

            <p className="mt-4 text-xs text-slate-500">
              Model <code>{result.sentiment.model_id}</code> • {result.sentiment.processing_time_ms} ms
            </p>

            <div className="mt-3 space-y-2">
              <Alert type="info">{result.sentiment.limitations}</Alert>
              {result.sentiment.warnings.map((w, i) => <Alert key={i} type="warning">{w}</Alert>)}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
