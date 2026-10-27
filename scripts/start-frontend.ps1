# Starts the Vite dev server on http://localhost:5173.
# Requires that scripts\setup-frontend.ps1 has been run once.
$ErrorActionPreference = "Stop"
$root     = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root "frontend"

if (-not (Test-Path (Join-Path $frontend "node_modules"))) {
    Write-Host "node_modules missing. Run scripts\setup-frontend.ps1 first." -ForegroundColor Red
    exit 1
}

Push-Location $frontend
try {
    Write-Host "Starting Vite dev server on http://localhost:5173 ..." -ForegroundColor Cyan
    npm run dev
} finally {
    Pop-Location
}
