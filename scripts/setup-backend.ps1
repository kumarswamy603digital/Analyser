# Creates backend/.venv and installs pinned requirements.
# Requires Python 3.10+ available as `python` on PATH.
$ErrorActionPreference = "Stop"
$root    = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root "backend"

Push-Location $backend
try {
    if (-not (Test-Path ".venv")) {
        Write-Host "Creating virtual environment at backend\.venv ..." -ForegroundColor Cyan
        python -m venv .venv
    }
    Write-Host "Upgrading pip ..." -ForegroundColor Cyan
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    Write-Host "Installing pinned dependencies (may take several minutes) ..." -ForegroundColor Cyan
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    Write-Host "Done. Start the backend with scripts\start-backend.ps1" -ForegroundColor Green
} finally {
    Pop-Location
}
