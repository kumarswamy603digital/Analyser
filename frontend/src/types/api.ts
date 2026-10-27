/** TypeScript types mirroring the backend Pydantic schemas. */

export interface LanguageInfo {
  code: string;
  name: string;
}

export interface SupportedPair {
  source: string;
  target: string;
  model_id: string;
}

export interface LanguagesResponse {
  languages: LanguageInfo[];
  directions: SupportedPair[];
  auto_detect_supported: boolean;
}

export interface ModelInfo {
  model_id: string;
  task: string;
  supported_languages: string[];
  labels: string[] | null;
  license: string;
  limitations: string;
}

export interface ModelsResponse {
  translation_models: ModelInfo[];
  sentiment_models: ModelInfo[];
}

export interface HealthResponse {
  status: string;
  version: string;
  readiness: {
    api_process: boolean;
    translation_model_ready: boolean;
    sentiment_model_ready: boolean;
  };
}

export interface TranslateResponse {
  source_language: string;
  target_language: string;
  translated_text: string;
  model_id: string;
  processing_time_ms: number;
  warnings: string[];
}

export interface SentimentResponse {
  predicted_label: string;
  scores: Record<string, number>;
  model_id: string;
  language: string;
  processing_time_ms: number;
  limitations: string;
  warnings: string[];
}

export type SentimentTarget = "original" | "translated";

export interface AnalyseResponse {
  translation: TranslateResponse;
  sentiment: SentimentResponse;
  analysed_text: string;
  analysed_text_origin: SentimentTarget;
}

/** Structured error envelope returned by the backend for any failure. */
export interface ApiError {
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
  };
}
