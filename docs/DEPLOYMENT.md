# Deployment Guide

## Local Development (Windows)

### Prerequisites
- Python 3.14 (verified with 3.14.7)
- Microsoft Visual C++ Redistributable x64 (for PyTorch DLL)  
  Download: https://aka.ms/vs/17/release/vc_redist.x64.exe  
  (Installs msvcp140.dll, vcruntime140.dll, vcruntime140_1.dll)
- Node.js 18+ (LTS recommended; 24.x tested)
- Git (optional, for cloning)

### Backend Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env   # edit CORS if needed
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend is available at http://localhost:8000. Swagger docs at /docs.

First call to `/api/v1/translate` or `/api/v1/sentiment` triggers model download to
the local HF_HOME cache (~300 MB total for all models used in the first request).
Subsequent requests use cached weights.

### Frontend Setup

```powershell
cd frontend
npm install
copy .env.example .env.local   # VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

Frontend available at http://localhost:5173.

---

## Docker Deployment

> **Status: NOT verified in this environment** (Docker is not installed).  
> The files are provided as correct templates.

```powershell
docker compose up --build
```

- Backend exposed on host port 8000; frontend (nginx) on host port 5173.
- `VITE_API_BASE_URL=http://localhost:8000` is baked into the frontend JS at build
  time. The browser (running OUTSIDE containers) reaches the backend on the host.
  **Do not use `http://backend:8000`** here — that name is only resolvable between
  containers, not by the user's browser.
- If deployed to a remote server, update the build arg to the server's public URL.

### Volumes

`hf_cache` volume persists model weights across container restarts (avoids re-download).

---

## Cloud Deployment

The project requires:
- Python runtime with torch (CPU inference)
- Hugging Face model downloads at first start (~300 MB)
- RAM: ~2 GB recommended for model + inference

Suitable platforms:
- **Render.com** (web service, Python): deploy backend; set CORS_ORIGINS to frontend URL.
- **Hugging Face Spaces**: Gradio or Docker Space; simpler but may not support FastAPI directly.
- **AWS Lambda + Container Image**: heavy cold start due to model size; not recommended.
- **VPS / Azure App Service**: any Docker-capable VM with enough RAM.

Deployment was NOT attempted because platform accounts are not available. Documented
for reference.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `OSError: c10.dll` not found | Install VC++ Redistributable x64 (system32 reboot may be needed) |
| `ModuleNotFoundError: transformers` | Ensure venv activated; re-run pip install |
| Frontend proxy error / CORS | Set `CORS_ORIGINS` in backend .env to include frontend URL |
| Model download very slow | Use a local HF mirror or pre-cache weights; set HF_ENDPOINT |
| `node` not recognized | Reinstall Node.js or add to PATH; restart terminal |
