import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";

// Mock the API service module to avoid actual network calls.
vi.mock("../services/api", () => ({
  getLanguages: vi.fn().mockResolvedValue({
    languages: [
      { code: "en", name: "English" },
      { code: "fr", name: "French" },
      { code: "hi", name: "Hindi" },
      { code: "es", name: "Spanish" },
    ],
    directions: [],
    auto_detect_supported: false,
  }),
  translate: vi.fn(),
  sentiment: vi.fn(),
  analyse: vi.fn(),
  getModels: vi.fn().mockResolvedValue({
    translation_models: [],
    sentiment_models: [{ model_id: "test", labels: ["NEGATIVE","POSITIVE"], limitations: "test" }],
  }),
  getHealth: vi.fn(),
  NetworkError: class extends Error {},
  BackendError: class extends Error {
    code = "test"; status = 400; details = {};
  },
}));

import Translator from "../pages/Translator";
import Sentiment from "../pages/Sentiment";
import { translate, sentiment } from "../services/api";

function renderPage(page: React.ReactNode) {
  return render(<MemoryRouter>{page}</MemoryRouter>);
}

describe("Translator", () => {
  beforeEach(() => vi.clearAllMocks());

  it("shows error on empty input", async () => {
    renderPage(<Translator />);
    fireEvent.click(screen.getByRole("button", { name: /translate/i }));
    await waitFor(() => expect(screen.getByText(/enter text/i)).toBeInTheDocument());
  });

  it("calls translate API and displays result", async () => {
    vi.mocked(translate).mockResolvedValueOnce({
      source_language: "en", target_language: "fr", translated_text: "Bonjour",
      model_id: "test-model", processing_time_ms: 10, warnings: [],
    });
    renderPage(<Translator />);
    const textarea = screen.getByLabelText(/source text/i);
    fireEvent.change(textarea, { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: /translate/i }));
    await waitFor(() => expect(screen.getByText("Bonjour")).toBeInTheDocument());
  });

  it("swap button exchanges languages", async () => {
    renderPage(<Translator />);
    await waitFor(() => expect(screen.getByLabelText(/source language/i)).toHaveValue("en"));
    fireEvent.click(screen.getByLabelText(/swap languages/i));
    expect(screen.getByLabelText(/source language/i)).toHaveValue("fr");
    expect(screen.getByLabelText(/target language/i)).toHaveValue("en");
  });
});

describe("Sentiment", () => {
  beforeEach(() => vi.clearAllMocks());

  it("shows error on empty input", async () => {
    renderPage(<Sentiment />);
    fireEvent.click(screen.getByRole("button", { name: /analyse/i }));
    await waitFor(() => expect(screen.getByText(/enter text/i)).toBeInTheDocument());
  });

  it("displays positive result", async () => {
    vi.mocked(sentiment).mockResolvedValueOnce({
      predicted_label: "positive", scores: { positive: 0.92, negative: 0.08 },
      model_id: "m", language: "en", processing_time_ms: 5,
      limitations: "English-only", warnings: [],
    });
    renderPage(<Sentiment />);
    const textarea = screen.getByLabelText(/english text/i);
    fireEvent.change(textarea, { target: { value: "I love it" } });
    fireEvent.click(screen.getByRole("button", { name: /analyse/i }));
    await waitFor(() => expect(screen.getByText(/positive/i)).toBeInTheDocument());
  });
});
