# Installs frontend dependencies (npm install).
# Requires Node.js 20+ and npm on PATH.
$ErrorActionPreference = "Stop"
$root     = Split-Path -Parent $PSScriptRoot
$frontend = Join-Path $root "frontend"

Push-Location $frontend
try {
    Write-Host "Installing npm packages (this may take a couple of minutes) ..." -ForegroundColor Cyan
    npm install
    Write-Host "Done. Start the dev server with scripts\start-frontend.ps1" -ForegroundColor Green
} finally {
    Pop-Location
}
