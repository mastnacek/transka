# DeepL Translator - PowerShell Spouštěcí Script (bez konzole)

# Kontrola .env souboru
if (-not (Test-Path .env)) {
    Write-Host "[VAROVÁNÍ] .env soubor neexistuje!" -ForegroundColor Yellow
    Write-Host "Spusťte nejprve: .\install.ps1" -ForegroundColor White
    Read-Host "Stiskněte Enter"
    exit 1
}

# Kontrola uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[CHYBA] uv není nainstalováno!" -ForegroundColor Red
    Read-Host "Stiskněte Enter"
    exit 1
}

# Spuštění aplikace BEZ konzole pomocí pythonw
# pythonw = Python bez konzole (Windows GUI mode)
Write-Host "Spouštím DeepL Translator..." -ForegroundColor Green

# Pomocí uv run s pythonw a module syntax
Start-Process -FilePath "uv" -ArgumentList "run", "pythonw", "-m", "src.main" -WindowStyle Hidden

# Ukončení PowerShell okna
exit
