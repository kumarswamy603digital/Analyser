# Starts the FastAPI backend for local development.
# Requires: Python 3.10+ and a virtual environment at backend/.venv
$ErrorActionPreference = "Stop"
$root    = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"
$venvPy  = Join-Path $backend ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPy)) {
    Write-Host "Virtual env not found. Run scripts/setup-backend.ps1 first." -ForegroundColor Red
    exit 1
}

Push-Location $backend
try {
    Write-Host "Starting uvicorn on http://localhost:8000 ..." -ForegroundColor Cyan
    & $venvPy -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
} finally {
    Pop-Location
}
