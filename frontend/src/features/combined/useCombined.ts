import { useState, useCallback } from "react";
import { analyse, BackendError, NetworkError } from "../../services/api";
import type { AnalyseResponse, SentimentTarget } from "../../types/api";

export function useCombined() {
  const [source, setSource] = useState("fr");
  const [target, setTarget] = useState("en");
  const [sentTarget, setSentTarget] = useState<SentimentTarget>("translated");
  const [input, setInput] = useState("");
  const [result, setResult] = useState<AnalyseResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed) { setError("Please enter text."); return; }
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      setResult(await analyse(trimmed, source, target, sentTarget));
    } catch (e) {
      if (e instanceof BackendError) setError(`${e.code}: ${e.message}`);
      else if (e instanceof NetworkError) setError(e.message);
      else setError("Unexpected error.");
    } finally {
      setLoading(false);
    }
  }, [input, source, target, sentTarget]);

  const clear = useCallback(() => {
    setInput("");
    setResult(null);
    setError(null);
  }, []);

  return {
    source, setSource,
    target, setTarget,
    sentTarget, setSentTarget,
    input, setInput,
    result, loading, error,
    run, clear,
  };
}
