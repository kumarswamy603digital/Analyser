# Frontend

React + TypeScript + Vite + Tailwind CSS application for the Translator & Sentiment Analyser.

## Development

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open http://localhost:5173/

## Build

```bash
npm run build
```

Output goes to `dist/` (static files, servable by any CDN or nginx).

## Testing

```bash
npm run test:run
```

Uses Vitest + React Testing Library with mocked API calls.

## Structure

- `src/pages/` — Translator, Sentiment, Combined, About
- `src/components/` — Button, Card, Alert, ScoreBar
- `src/hooks/` — useTheme, useLanguages
- `src/services/api.ts` — typed fetch client
- `src/types/api.ts` — mirrors backend Pydantic schemas
- `src/test/` — Vitest setup + test files
