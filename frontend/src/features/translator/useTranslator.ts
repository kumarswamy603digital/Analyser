import { useState, useCallback } from "react";
import { translate, BackendError, NetworkError } from "../../services/api";
import type { TranslateResponse } from "../../types/api";

export interface TranslatorState {
  source: string;
  target: string;
  input: string;
  result: TranslateResponse | null;
  loading: boolean;
  error: string | null;
}

export function useTranslator() {
  const [source, setSource] = useState("en");
  const [target, setTarget] = useState("fr");
  const [input, setInput] = useState("");
  const [result, setResult] = useState<TranslateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const swap = useCallback(() => {
    setSource(target);
    setTarget(source);
    if (result) {
      setInput(result.translated_text);
      setResult(null);
    }
  }, [source, target, result]);

  const run = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed) { setError("Please enter text to translate."); return; }
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      const res = await translate(trimmed, source, target);
      setResult(res);
    } catch (e) {
      if (e instanceof BackendError) setError(`${e.code}: ${e.message}`);
      else if (e instanceof NetworkError) setError(e.message);
      else setError("An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  }, [input, source, target]);

  const clear = useCallback(() => {
    setInput("");
    setResult(null);
    setError(null);
  }, []);

  return { source, setSource, target, setTarget, input, setInput, result, loading, error, swap, run, clear };
}
