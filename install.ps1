# DeepL Translator - PowerShell Instalační Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DeepL Translator - Instalace" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kontrola uv
Write-Host "[1/3] Kontrola uv..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[CHYBA] uv není nainstalováno!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Nainstalujte uv pomocí:" -ForegroundColor Yellow
    Write-Host "  irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor White
    Write-Host ""
    Read-Host "Stiskněte Enter pro ukončení"
    exit 1
}

uv --version
Write-Host ""

# Synchronizace závislostí
Write-Host "[2/3] Synchronizace závislostí..." -ForegroundColor Yellow
uv sync

if ($LASTEXITCODE -ne 0) {
    Write-Host "[CHYBA] Instalace závislostí selhala!" -ForegroundColor Red
    Read-Host "Stiskněte Enter pro ukončení"
    exit 1
}

Write-Host ""

# Vytvoření .env souboru
Write-Host "[3/3] Vytváření .env souboru..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host ".env soubor vytvořen - NEZAPOMEŇTE PŘIDAT DEEPL API KLÍČ!" -ForegroundColor Green
} else {
    Write-Host ".env soubor již existuje" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalace dokončena!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Další kroky:" -ForegroundColor Yellow
Write-Host "1. Otevřete .env a přidejte DEEPL_API_KEY" -ForegroundColor White
Write-Host "2. Spusťte aplikaci pomocí: .\start.ps1" -ForegroundColor White
Write-Host ""
Read-Host "Stiskněte Enter pro ukončení"
