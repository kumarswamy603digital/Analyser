import { useSentiment } from "../features/sentiment/useSentiment";
import Card from "../components/Card";
import Button from "../components/Button";
import Alert from "../components/Alert";
import ScoreBar from "../components/ScoreBar";

const MAX_CHARS = 1000;

export default function Sentiment() {
  const { input, setInput, result, loading, error, run, clear } = useSentiment();
  const confidence = result ? Math.max(...Object.values(result.scores)) : 0;

  return (
    <div className="mx-auto w-full max-w-3xl space-y-4">
      <h1 className="text-2xl font-bold">Sentiment Analysis</h1>

      <Card>
        <label className="label" htmlFor="sent-text">English text</label>
        <textarea
          id="sent-text"
          className="textarea min-h-32"
          placeholder="Type a positive or negative English sentence..."
          maxLength={MAX_CHARS}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <div className="mt-1 text-xs text-slate-500">
          {input.length} / {MAX_CHARS} characters. English-only (DistilBERT SST-2).
        </div>
        <div className="mt-4 flex gap-2">
          <Button onClick={run} disabled={loading} variant="primary">
            {loading ? "Analysing…" : "Analyse Sentiment"}
          </Button>
          <Button onClick={clear} disabled={loading} variant="ghost">Clear</Button>
        </div>
        {error && <div className="mt-4"><Alert type="error">{error}</Alert></div>}
      </Card>

      {result && (
        <Card title="Result">
          <div className="flex items-center justify-between gap-4">
            <div>
              <span className="text-sm text-slate-500">Predicted label</span>
              <div className="mt-1">
                <span className={"badge badge-lg " +
                  (result.predicted_label === "positive" ? "badge-success" : "badge-error")}>
                  {result.predicted_label.toUpperCase()}
                </span>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">{confidence.toFixed(2)}</div>
              <div className="text-xs text-slate-500">confidence (top score)</div>
            </div>
          </div>

          <div className="mt-5">
            <ScoreBar scores={result.scores} />
          </div>

          <div className="mt-4 text-xs text-slate-500">
            Model <code>{result.model_id}</code> • {result.processing_time_ms} ms •
            Language <code>{result.language}</code>
          </div>

          <div className="mt-3 space-y-2">
            <Alert type="info">{result.limitations}</Alert>
            {result.warnings.map((w, i) => <Alert key={i} type="warning">{w}</Alert>)}
          </div>
        </Card>
      )}

      {!result && !loading && !error && (
        <Alert type="info">
          Try a clearly positive sentence (e.g. "I love this film!") or negative
          (e.g. "This is terrible.") and observe the confidence shift.
        </Alert>
      )}
    </div>
  );
}
