# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architektura projektu

**Transka** je desktop překladač s podporou DeepL a Google Translate API, postavený na **Tkinter GUI** s **system tray** a **globálními klávesovými zkratkami**.

### Hlavní komponenty

#### 1. **Abstrakce překladačů** (Strategy Pattern)
- `BaseTranslator` (base_translator.py) - abstraktní rozhraní
- `DeepLTranslator` (deepl_translator.py) - DeepL API implementace
- `GoogleTranslator` (google_translator.py) - Google Translate implementace
- **Přepínání** mezi překladači za běhu bez restartu (live reload)

#### 2. **GUI moduly**
- `app.py` - hlavní aplikace `TranslatorApp` (579 řádků)
  - 3-step workflow: otevři → přelož → zkopíruj+zavři
  - System tray integrace
  - Globální hotkeys registrace
  - Použití ThemeManager pro styling
- `settings_window.py` - samostatný modul pro nastavení (192 řádků)
  - `SettingsWindow` třída
  - Live reload podpory (změny se aplikují okamžitě)
  - Test API funkce
- `theme_manager.py` - správa dark theme (147 řádků)
  - `ThemeManager` třída
  - Aplikace dark titlebar (Windows 11/10)
  - Font management (Fira Code, Consolas fallback)
  - TTK styles konfigurace pro dark mode

#### 3. **GUI workflow** (3-step process)
Hlavní logika v `app.py::TranslatorApp`:
```
1. První Win+P / Ctrl+P+P → Otevře okno
2. Druhý Win+P / Ctrl+P+P → Přeloží text (okno zůstane otevřené)
3. Třetí Win+P / Ctrl+P+P → Zkopíruje překlad + zavře okno + vrátí fokus
```

#### 4. **Konfigurace** (config.py)
- `config.json` - uživatelská nastavení (jazyk, překladač, zkratky, GUI rozměry)
- `.env` - DeepL API klíč (pouze pro DeepL, Google nepotřebuje)
- `Config` třída: singleton-like správce nastavení s `load()` / `save()`

#### 5. **System tray** (pystray)
- `create_image()` - generování ikony programově (Image + ImageDraw)
- Menu: Zobrazit / Nastavení / Ukončit
- Globální zkratky: `keyboard` knihovna pro Win+P registraci

### Klíčové flow

```
app.py::main()
  → Config.load()
  → TranslatorApp(config)
    → _create_translator() # DeepL nebo Google podle config
    → _setup_ui() # Tkinter GUI + dark theme
    → _setup_tray() # System tray ikona
    → _setup_hotkeys() # Globální Win+P / Ctrl+P+P
    → root.mainloop()
```

**Workflow states:**
- `workflow_state` enum: `INITIAL`, `TRANSLATED`, `READY_TO_CLOSE`
- State transitions: hotkey mění stav podle aktuálního workflow step

### Dark theme

- `theme.py` - konstanty (`COLORS` dict + `FONTS` dict)
- `theme_manager.py` - aplikační logika (`ThemeManager` třída)
  - Centralizovaná správa theme pro všechna okna
  - Dark titlebar pro Windows (ctypes DwmSetWindowAttribute)
  - Font management s fallback systémem
- Cyberpunk styl: tmavé pozadí (#1a1a2e), neonové akcenty (#00d9ff, #ff006e)
- Font: Fira Code (fallback na Consolas/Courier)

## Development příkazy

### Instalace

**UV (doporučeno):**
```bash
# První instalace
install.bat  # Spustí: uv sync + vytvoří .env

# Nebo manuálně
uv sync
copy .env.example .env
```

**Pip (fallback):**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Spuštění

```bash
# Běžné spuštění (bez konzole)
start.bat  # Spustí: uv run pythonw -m transka

# Spuštění s konzolí (debugging)
uv run python -m transka

# Klasické spuštění (bez uv)
.venv\Scripts\activate
pythonw -m transka  # Bez konzole
python -m transka   # S konzolí pro debugging

# Po instalaci jako package
uv sync
deepl-translator  # Console script z pyproject.toml
```

### Debugging

```bash
# Spuštění s debug výstupem (zobrazí traceback, print statements)
uv run python -m transka

# Testování importů
uv run python -c "from transka.app import main; print('OK')"

# Kontrola konfigurace
cat config.json
cat .env
```

### Dependencies management

```bash
# Přidat novou závislost
uv add <package-name>

# Upgrade závislostí
uv lock --upgrade

# Synchronizace (po git pull)
uv sync
```

## Důležité poznámky pro úpravy

### Globální zkratky
- **Windows API závislost**: `keyboard` knihovna může vyžadovat admin práva na některých systémech
- **Registrace**: `keyboard.add_hotkey()` v `_setup_hotkeys()`
- **Unregister**: vždy zavolat `keyboard.remove_hotkey()` před změnou zkratky

### Live reload překladače
- Změna `translator_service` v Settings → okamžitě volá `_switch_translator()`
- **NESMÍ** restartovat aplikaci - musí zachovat GUI state
- Nový translator instance se vytvoří v `_create_translator(service_name)`

### API Usage tracking
- **DeepL**: má limit 500k znaků/měsíc → zobrazuje usage bar
- **Google**: neomezený → usage bar skrytý
- `UsageInfo` dataclass: `character_count`, `character_limit`, `usage_percentage`

### Threading
- **System tray běží v separátním threadu**: `threading.Thread(target=icon.run, daemon=True)`
- **Tkinter main thread**: GUI updates MUSÍ být v main thread
- **Hotkeys**: `keyboard` používá vlastní thread pool

### Packaging
- `pyproject.toml` - modern Python package config
- Console script: `deepl-translator = "transka.app:main"`
- Package structure: `src/transka/` layout (PEP 420 compatible)

## Testování změn

Po úpravě kódu:
```bash
# Testuj import
uv run python -c "from transka.app import main"

# Spusť s konzolí (vidíš errory)
uv run python -m transka

# Testuj změnu překladače
# → otevři Settings → přepni DeepL/Google → překlad by měl fungovat
```

## Tech stack shrnutí

- **GUI**: Tkinter (stdlib, cross-platform)
- **System tray**: pystray + Pillow (ikona generována kódem)
- **Hotkeys**: keyboard (Win32 API wrapper)
- **Překladače**: deepl-python, googletrans
- **Config**: python-dotenv + JSON storage
- **Clipboard**: pyperclip
- **Package manager**: uv (fallback: pip)
