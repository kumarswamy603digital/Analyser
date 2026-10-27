# Runs backend (pytest) and frontend (vitest) test suites.
# Backend fast tests should pass without torch inference; smoke tests
# (marked `slow`) require the Microsoft Visual C++ Redistributable to be
# installed so that torch can import.
$ErrorActionPreference = "Continue"
$root     = Split-Path -Parent $PSScriptRoot
$backend  = Join-Path $root "backend"
$frontend = Join-Path $root "frontend"
$venvPy   = Join-Path $backend ".venv\Scripts\python.exe"

Write-Host "`n=== Backend tests (fast, deselect slow) ===" -ForegroundColor Cyan
Push-Location $backend
try {
    & $venvPy -m pytest -q
} finally { Pop-Location }

Write-Host "`n=== Backend smoke tests (real model inference) ===" -ForegroundColor Cyan
Write-Host "  Requires: Microsoft Visual C++ Redistributable + torch installed." -ForegroundColor DarkGray
Push-Location $backend
try {
    & $venvPy -m pytest -m slow -q
} finally { Pop-Location }

Write-Host "`n=== Frontend tests (Vitest) ===" -ForegroundColor Cyan
Write-Host "  Requires: Node.js + npm install already completed." -ForegroundColor DarkGray
Push-Location $frontend
try {
    npm run test:run
} finally { Pop-Location }
