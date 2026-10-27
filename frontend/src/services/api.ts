/**
 * Typed API client. All backend calls go through this module; presentation
 * components never call fetch directly.
 */
import type {
  ApiError,
  AnalyseResponse,
  HealthResponse,
  LanguagesResponse,
  ModelsResponse,
  SentimentResponse,
  SentimentTarget,
  TranslateResponse,
} from "../types/api";

const BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class NetworkError extends Error {
  constructor(msg = "Network error: backend unreachable.") {
    super(msg);
    this.name = "NetworkError";
  }
}

export class BackendError extends Error {
  code: string;
  status: number;
  details: Record<string, unknown>;

  constructor(err: ApiError["error"], status: number) {
    super(err.message);
    this.code = err.code;
    this.status = status;
    this.details = err.details;
    this.name = "BackendError";
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let resp: Response;
  try {
    resp = await fetch(`${BASE}${path}`, {
      headers: { "Content-Type": "application/json", ...options?.headers },
      ...options,
    });
  } catch {
    throw new NetworkError();
  }

  if (!resp.ok) {
    let body: ApiError;
    try {
      body = await resp.json();
    } catch {
      throw new BackendError(
        { code: "unknown", message: resp.statusText, details: {} },
        resp.status
      );
    }
    throw new BackendError(body.error, resp.status);
  }

  return resp.json() as Promise<T>;
}

// --- Public methods ---

export function getHealth() {
  return request<HealthResponse>("/health");
}

export function getLanguages() {
  return request<LanguagesResponse>("/api/v1/languages");
}

export function getModels() {
  return request<ModelsResponse>("/api/v1/models");
}

export function translate(text: string, source: string, target: string) {
  return request<TranslateResponse>("/api/v1/translate", {
    method: "POST",
    body: JSON.stringify({ text, source_language: source, target_language: target }),
  });
}

export function sentiment(text: string) {
  return request<SentimentResponse>("/api/v1/sentiment", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

export function analyse(
  text: string,
  source: string,
  target: string,
  sentimentTarget: SentimentTarget
) {
  return request<AnalyseResponse>("/api/v1/analyse", {
    method: "POST",
    body: JSON.stringify({
      text,
      source_language: source,
      target_language: target,
      sentiment_target: sentimentTarget,
    }),
  });
}
