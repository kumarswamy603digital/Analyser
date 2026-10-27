import { useState, useCallback } from "react";
import { sentiment, BackendError, NetworkError } from "../../services/api";
import type { SentimentResponse } from "../../types/api";

export function useSentiment() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<SentimentResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(async () => {
    const trimmed = input.trim();
    if (!trimmed) { setError("Please enter text to analyse."); return; }
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      setResult(await sentiment(trimmed));
    } catch (e) {
      if (e instanceof BackendError) setError(`${e.code}: ${e.message}`);
      else if (e instanceof NetworkError) setError(e.message);
      else setError("Unexpected error.");
    } finally {
      setLoading(false);
    }
  }, [input]);

  const clear = useCallback(() => { setInput(""); setResult(null); setError(null); }, []);

  return { input, setInput, result, loading, error, run, clear };
}
