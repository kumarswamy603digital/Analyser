import { useEffect, useState } from "react";
import { getLanguages, NetworkError } from "../services/api";
import type { LanguagesResponse } from "../types/api";

/**
 * Fetches supported languages on mount. Caches in memory per component lifetime.
 */
export function useLanguages() {
  const [data, setData] = useState<LanguagesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    getLanguages()
      .then((res) => { if (!cancelled) setData(res); })
      .catch((e) => {
        if (cancelled) return;
        setError(e instanceof NetworkError ? "Backend unreachable." : e.message);
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  return { data, error, loading };
}
