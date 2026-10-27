import { Link } from "react-router-dom";
import { useLanguages } from "../hooks/useLanguages";
import { useTranslator } from "../features/translator/useTranslator";
import Card from "../components/Card";
import Button from "../components/Button";
import Alert from "../components/Alert";
import type { LanguageInfo } from "../types/api";

const MAX_CHARS = 1000;

function LangSelect({ value, onChange, languages, ariaLabel }: {
  value: string; onChange: (v: string) => void; languages: LanguageInfo[]; ariaLabel: string;
}) {
  return (
    <select aria-label={ariaLabel} className="select" value={value} onChange={(e) => onChange(e.target.value)}>
      {languages.map((l) => <option key={l.code} value={l.code}>{l.name}</option>)}
    </select>
  );
}

export default function Translator() {
  const { data: langs } = useLanguages();
  const { source, setSource, target, setTarget, input, setInput,
    result, loading, error, swap, run, clear } = useTranslator();

  const languages = langs?.languages ?? [];
  const directionOk = !langs
    ? true
    : langs.directions.some(d => d.source === source && d.target === target);

  return (
    <div className="mx-auto w-full max-w-3xl space-y-4">
      <h1 className="text-2xl font-bold">Translator</h1>

      <Card>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-500">From</span>
            <LangSelect ariaLabel="Source language" value={source} onChange={setSource} languages={languages} />
          </div>
          <button
            type="button"
            onClick={swap}
            className="btn btn-ghost btn-sm"
            title="Swap languages"
            aria-label="Swap languages"
          >
            ⇄
          </button>
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-500">To</span>
            <LangSelect ariaLabel="Target language" value={target} onChange={setTarget} languages={languages} />
          </div>
        </div>

        <p className="mt-2 text-xs text-slate-500">
          If the chosen direction is unsupported the backend returns a clear 400 error.
        </p>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <div>
            <label className="label" htmlFor="src-text">Source text</label>
            <textarea
              id="src-text"
              className="textarea min-h-40"
              placeholder="Enter text to translate..."
              maxLength={MAX_CHARS}
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <div className="mt-1 text-xs text-slate-500">
              {input.length} / {MAX_CHARS} characters
            </div>
          </div>
          <div>
            <label className="label">Translated output</label>
            <textarea
              readOnly
              className="textarea min-h-40 bg-slate-100 dark:bg-slate-800"
              placeholder="Translation will appear here"
              value={result?.translated_text ?? ""}
            />
            {result && (
              <div className="mt-1 text-xs text-slate-500">
                {result.model_id} • {result.processing_time_ms} ms
              </div>
            )}
          </div>
        </div>

        <div className="mt-4 flex gap-2">
          <Button onClick={run} disabled={loading} variant="primary">
            {loading ? "Translating…" : "Translate"}
          </Button>
          <Button onClick={clear} disabled={loading} variant="ghost">Clear</Button>
        </div>

        {error && <div className="mt-4"><Alert type="error">{error}</Alert></div>}
      </Card>

      {result && (
        <Card title="Result">
          <pre className="whitespace-pre-wrap break-words rounded-md bg-slate-100 p-3 font-mono text-sm dark:bg-slate-800">
            {result.translated_text}
          </pre>
          {result.warnings.length > 0 && (
            <div className="mt-3 space-y-2">
              {result.warnings.map((w, i) => <Alert key={i} type="warning">{w}</Alert>)}
            </div>
          )}
        </Card>
      )}

      {!directionOk && (
        <Alert type="warning">
          <code>{source} → {target}</code> is not a supported direction.
          Visit the <Link to="/about" className="underline">About</Link> page for the full matrix.
        </Alert>
      )}
    </div>
  );
}
