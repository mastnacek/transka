@echo off
REM Instalace DeepL Translator pomoci uv

echo ========================================
echo DeepL Translator - Instalace
echo ========================================
echo.

REM Kontrola uv
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [CHYBA] uv neni nainstalovano!
    echo.
    echo Nainstalujte uv pomoci:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    pause
    exit /b 1
)

echo [1/3] Kontrola uv...
uv --version

echo.
echo [2/3] Synchronizace zavislosti...
uv sync

echo.
echo [3/3] Vytvareni .env souboru...
if not exist .env (
    copy .env.example .env
    echo .env soubor vytvoren - NEZAPOMENTE PRIDAT DEEPL API KLIC!
) else (
    echo .env soubor jiz existuje
)

echo.
echo ========================================
echo Instalace dokoncena!
echo ========================================
echo.
echo Dalsi kroky:
echo 1. Otevrete .env a pridejte DEEPL_API_KEY
echo 2. Spustte aplikaci pomoci: start.bat
echo.
pause
