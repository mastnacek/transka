# Transka - Desktop Translator

**Rychlá desktopová aplikace pro okamžitý překlad textů** - ideální pro překlad promptů pro AI asistenty (Claude, ChatGPT) a práci s kódem.

Moderní desktop aplikace pro rychlý překlad s podporou **DeepL** a **Google Translate** API, dark theme a intuitivními klávesovými zkratkami.

## 🎯 Účel aplikace

**Transka vznikla pro rychlý překlad textů při práci s AI:**
- ✅ **Překlad promptů**: Rychle přeložit české zadání pro anglické AI (Claude Code, ChatGPT)
- ✅ **Překlad odpovědí AI**: Okamžitý překlad anglických odpovědí do češtiny
- ✅ **Práce s kódem**: Překlad komentářů, dokumentace, commit messages
- ✅ **3-krokový workflow**: Otevři (Ctrl+P+P) → Přelož (Ctrl+P+P) → Zkopíruj do schránky (Ctrl+P+P)
- ✅ **System tray**: Běží na pozadí, okamžitě dostupný globální zkratkou

## 🚀 Funkce

- **Dva překladače na výběr**:
  - **DeepL API** - Vysoká kvalita, vyžaduje API klíč (Free: 500k znaků/měsíc)
  - **Google Translate** - Zdarma bez API klíče, neomezené použití
- **System Tray**: Aplikace běží na pozadí v system tray
- **Klávesové zkratky**:
  - **`Ctrl+P+P`** - Hlavní zkratka (dvojité rychlé stisknutí Ctrl+P < 0.5s)
    - 1. stisk = otevře okno
    - 2. stisk = přeloží text
    - 3. stisk = zkopíruje a zavře
  - **`ESC`** - Zavře okno bez překladu
  - **`Ctrl+Enter`** - Přeloží text v okně (legacy)
- **Automatické vymazání**: Input pole se automaticky vymaže po úspěšném překladu
- **Počítadlo znaků**: Sledování spotřeby API (DeepL zobrazuje usage, Google je neomezený)
- **Varování při limitu**: Upozornění při dosažení 96% limitu (DeepL)
- **Modern Dark Theme**: Cyberpunk design s Fira Code fontem
- **Live reload**: Změny nastavení (včetně překladače) se aplikují okamžitě
- **Konfigurovatelné**: Nastavení jazyků, překladače, API klíče a zkratek

## 📋 Požadavky

- Python 3.8+
- **DeepL API klíč** (Free nebo Pro) - **pouze pokud chcete používat DeepL**
- **Google Translate** - funguje bez API klíče, zdarma
- Windows (kvůli system tray a globálním zkratkám)

## 🔧 Instalace

### Varianta A: Pomocí UV (doporučeno)

1. **Nainstalujte UV** (pokud ještě nemáte):
```bash
# PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Nebo curl (Git Bash)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Spusťte instalační script**:
```bash
install.bat
```

3. **Nastavte DeepL API klíč** v `.env` souboru:
```
DEEPL_API_KEY=your-actual-api-key-here
```

4. **Spusťte aplikaci**:
```bash
start.bat
```

### Varianta B: Klasická instalace pomocí pip

1. **Vytvořte virtuální prostředí**:
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Nainstalujte závislosti**:
```bash
pip install -r requirements.txt
```

3. **Vytvořte `.env` soubor**:
```bash
copy .env.example .env
```

4. **Vložte DeepL API klíč** do `.env`:
```
DEEPL_API_KEY=your-actual-api-key-here
```

5. **Spusťte aplikaci**:
```bash
# Bez konzole (doporučeno)
pythonw -m transka

# S konzolí (pro debugging)
python -m transka
```

## 🎯 Jak získat DeepL API klíč

1. Navštivte [DeepL API Free](https://www.deepl.com/pro-api)
2. Zaregistrujte se pro Free API (500,000 znaků/měsíc zdarma)
3. Zkopírujte API klíč z dashboardu
4. Vložte do `.env` souboru

## 🏃 Spuštění

### Pomocí UV:
```bash
start.bat
```

### Klasicky:
```bash
# Bez konzole (doporučeno - aplikace běží na pozadí)
pythonw -m transka

# S konzolí (pro debugging)
python -m transka
```

### Po instalaci jako package:
```bash
# Spustitelný příkaz (po: uv sync nebo pip install -e .)
transka
```

Aplikace se spustí v system tray. Klikněte na ikonu pro otevření menu.

## ⚙️ Nastavení

- **Překladač**: Výběr mezi `deepl` a `google`
  - **DeepL**: Vyžaduje API klíč, vyšší kvalita, limit 500k znaků/měsíc
  - **Google**: Zdarma, bez API klíče, neomezené použití
- **API klíč**: DeepL API klíč (Free nebo Pro) - pouze pro DeepL
- **Zdrojový jazyk**: Jazyk vstupního textu (AUTO pro automatickou detekci)
- **Cílový jazyk**: Jazyk překladu
- **Klávesová zkratka**: Hlavní zkratka (výchozí: Ctrl+P+P double-press, lze změnit)
- **Práh varování**: Limit znaků pro varování - pouze pro DeepL (výchozí: 480,000)

## 🎮 Použití

### Hlavní workflow (3-step s Ctrl+P+P):

**Workflow se třemi kroky pomocí dvojitého Ctrl+P:**

1. **První `Ctrl+P+P`** (stisknout Ctrl+P dvakrát rychle) → **Otevře okno**
   - Okno se zobrazí s fokusem na input poli
   - Vložte text k překladu

2. **Druhý `Ctrl+P+P`** → **Přeloží text**
   - Text se přeloží a zobrazí v "Přeložený text" poli
   - **Okno zůstane otevřené** - můžete si prohlédnout překlad

3. **Třetí `Ctrl+P+P`** → **Zkopíruje a zavře**
   - Překlad se zkopíruje do schránky
   - Input pole se vymaže
   - Okno se zavře
   - **Fokus se vrátí na předchozí program** (kde jste byli před otevřením)

**Příklad použití:**
```
1. Ctrl+P+P → okno se otevře
2. Napíšete: "Ahoj světe"
3. Ctrl+P+P → zobrazí: "Hello world"
4. Ctrl+P+P → zkopíruje "Hello world", zavře okno, vrátí fokus
5. Ctrl+V → vložíte překlad kam potřebujete
```

### Alternativní zkratky:
- **`ESC`**: Zavře okno kdykoli (resetuje workflow)
- **`Ctrl+Enter`**: Přeloží text v okně (okno zůstane otevřené, state se NEMĚNÍ)
  - **Smart workflow**: Další `Ctrl+P+P` detekuje přeložený text a rovnou zkopíruje + zavře
- **Tlačítko "Přeložit"**: Stejné jako Ctrl+Enter

**💡 Tip**: Kombinujte Ctrl+Enter s Ctrl+P+P pro flexibilní workflow!

### 🎯 Smart Detection:

**Ctrl+P+P v state SHOWN inteligentně detekuje přeložený text:**
- ✅ **Existuje překlad v output poli** → přeskoč překlad, zkopíruj a zavři (šetří čas!)
- ❌ **Prázdné output pole** → normálně přelož (klasický 3-step workflow)

**Příklad použití:**
```
1. Ctrl+P+P → otevře okno
2. Napíšete text + Ctrl+Enter → přeloží (zkontrolujete překlad)
3. Ctrl+P+P → detekuje překlad → zkopíruje a zavře (skip kroku 2!)
```

## 💼 Praktické použití (Use Cases)

### 1. Překlad promptu pro AI asistenta (Claude Code, ChatGPT)

**Scénář:** Chcete poslat českému zadání anglickému AI asistentovi.

```
1. Napíšete v Czechu: "Vytvoř mi funkci na validaci emailu"
2. Ctrl+P+P → otevře Transka
3. Ctrl+V → vložíte text
4. Ctrl+P+P → přeloží: "Create a function for email validation"
5. Ctrl+P+P → zkopíruje do schránky + zavře okno
6. Ctrl+V → vložíte překlad do AI chatu
```

### 2. Překlad odpovědi AI do češtiny

**Scénář:** AI odpověděl anglicky a chcete to rychle přeložit.

```
1. Označíte anglickou odpověď AI
2. Ctrl+C → zkopírujete
3. Ctrl+P+P → otevře Transka (text se automaticky vloží)
4. Ctrl+P+P → přeloží do češtiny
5. Ctrl+P+P → zkopíruje překlad
6. Máte český překlad v clipboardu
```

### 3. Překlad commit message

**Scénář:** Píšete commit v angličtině, ale myslíte česky.

```
1. Myslíte: "Oprava chyby v autentifikaci"
2. Ctrl+P+P → otevře Transka
3. Napíšete česky
4. Ctrl+P+P → přeloží: "Fix authentication bug"
5. Ctrl+P+P → zkopíruje
6. git commit -m <Ctrl+V>
```

### 4. Překlad dokumentace/komentářů

**Scénář:** Čtete anglickou dokumentaci a potřebujete rychlý překlad.

```
1. Označíte text v dokumentaci
2. Ctrl+C
3. Ctrl+P+P → otevře Transka
4. Ctrl+V → vloží
5. Ctrl+P+P → přeloží
6. Přečtete překlad v okně (okno zůstane otevřené)
7. ESC → zavře okno
```

### System Tray Menu:
- **Zobrazit**: Otevře překladové okno
- **Nastavení**: Otevře okno nastavení
- **Ukončit**: Ukončí aplikaci

## 📊 Počítadlo znaků

Aplikace zobrazuje aktuální spotřebu API:
- **Zelená** (0-80%): Normální spotřeba
- **Oranžová** (80-96%): Zvýšená spotřeba
- **Červená** (96-100%): Blízko limitu

Formát: `15,234 / 500,000 znaků (3.0%)`

## 🛠️ Technologie

- **Python 3.8+**
- **Tkinter**: GUI framework
- **DeepL API**: Překladová služba (volitelné)
- **Google Translate API** (`googletrans`): Free překladač bez API klíče
- **pystray**: System tray ikona
- **keyboard**: Globální klávesové zkratky
- **pyperclip**: Práce se schránkou

## 📝 Architektura projektu (Clean Code)

**Transka používá čistou modulární architekturu** s oddělením zodpovědností:

```
transka/
├── src/transka/
│   ├── app.py (301 řádků) ⭐ ORCHESTRÁTOR
│   │   └── TranslatorApp - koordinuje všechny managery
│   │
│   ├── GUI Layer:
│   │   ├── gui_builder.py (245 řádků)
│   │   │   └── GUIBuilder - Builder pattern pro vytvoření widgets
│   │   ├── settings_window.py (192 řádků)
│   │   │   └── SettingsWindow - okno nastavení s live reload
│   │   └── theme_manager.py (147 řádků)
│   │       └── ThemeManager - dark theme + Windows titlebar
│   │
│   ├── Business Logic:
│   │   └── translation_workflow.py (194 řádků)
│   │       └── TranslationWorkflow - state machine pro 3-step workflow
│   │           ├── STATE_HIDDEN → STATE_SHOWN → STATE_TRANSLATED
│   │           ├── Threading pro async překlady
│   │           └── Clipboard operations + focus management
│   │
│   ├── System Integration:
│   │   ├── hotkey_manager.py (81 řádků)
│   │   │   └── HotkeyManager - globální zkratky + double-press detection
│   │   └── tray_manager.py (72 řádků)
│   │       └── TrayManager - system tray ikona + menu
│   │
│   └── Translation Core:
│       ├── base_translator.py (93 řádků)
│       │   └── BaseTranslator - abstraktní rozhraní (Strategy Pattern)
│       ├── deepl_translator.py (144 řádků)
│       │   └── DeepLTranslator - DeepL API implementace
│       ├── google_translator.py (168 řádků)
│       │   └── GoogleTranslator - Google Translate implementace
│       └── config.py (124 řádků)
│           └── Config - správa konfigurace (JSON + .env)
│
├── install.bat               # Instalační script (uv sync)
├── start.bat                 # Spouštěcí script (pythonw bez konzole)
├── pyproject.toml            # Modern Python package konfigurace
├── requirements.txt          # Python závislosti (pip fallback)
├── .env                      # DeepL API klíč - gitignored
├── config.json               # Uživatelské nastavení - gitignored
└── README.md                 # Dokumentace
```

### 🏗️ Design Patterns použité:

1. **Dependency Injection** - app.py injektuje závislosti do managerů
2. **Builder Pattern** - GUIBuilder pro vytvoření GUI komponent
3. **Strategy Pattern** - BaseTranslator → DeepL/Google implementace
4. **State Machine** - TranslationWorkflow (3 stavy workflow)
5. **Single Responsibility** - každý modul má jednu zodpovědnost

### 🔧 Detailní popis modulů:

#### **app.py** - Orchestrátor (301 řádků)
- `TranslatorApp.__init__()` - inicializace všech managerů
- `_handle_main_hotkey()` - state machine pro 3-step workflow
- `_show_window()` / `_hide_window()` - window management + centrování
- `_update_usage()` - threading pro async update usage statistik
- `_on_settings_saved()` - callback pro live reload nastavení

#### **translation_workflow.py** - Business logika (194 řádků)
- `TranslationWorkflow` - hlavní třída pro překlad workflow
  - `translate_with_display()` - překlad bez kopírování (krok 2)
  - `translate_full()` - kompletní překlad (tlačítko Přeložit)
  - `copy_translation_and_clear()` - kopírování + cleanup (krok 3)
  - `save_previous_window()` / `restore_previous_window()` - focus management
  - State machine: `STATE_HIDDEN` → `STATE_SHOWN` → `STATE_TRANSLATED`

#### **hotkey_manager.py** - Klávesové zkratky (81 řádků)
- `HotkeyManager` - správa globálních zkratek
  - `register_hotkeys()` - registrace hlavní zkratky (výchozí: ctrl+p+p)
  - `_handle_ctrl_p()` - **double-press detection** (Ctrl+P dvakrát < 0.5s)
  - `update_main_hotkey()` - dynamická změna zkratky (live reload)
  - `unregister_all()` - cleanup při ukončení
  - **Poznámka**: Používá time tracking pro detekci dvojitého stisku

#### **gui_builder.py** - GUI konstrukce (245 řádků)
- `GUIBuilder` - Builder pattern pro vytvoření GUI
  - `build()` - hlavní metoda vytváření widgets
  - `_create_header()` - header s překladačem + jazyky
  - `_create_input_field()` / `_create_output_field()` - textová pole
  - `_create_status_bar()` - status + usage label
  - `_create_buttons()` - tlačítka s callbacky

#### **tray_manager.py** - System tray (72 řádků)
- `TrayManager` - správa system tray ikony
  - `start()` - spustí tray v separátním threadu
  - `_create_icon_image()` - generuje ikonu programově (PIL)
  - Menu: Zobrazit / Nastavení / Ukončit

#### **theme_manager.py** - Dark theme (147 řádků)
- `ThemeManager` - správa aplikačního stylu
  - `apply_theme()` - aplikuje kompletní dark theme
  - `_apply_dark_titlebar()` - Windows 11/10 dark titlebar (ctypes)
  - `_create_fonts()` - Fira Code + Consolas fallback
  - `_configure_ttk_styles()` - TTK widgets styling

#### **settings_window.py** - Nastavení (192 řádků)
- `SettingsWindow` - okno pro konfiguraci
  - `_save_settings()` - live reload (okamžitá aplikace změn)
  - `_test_api()` - test DeepL API připojení
  - Dynamic hotkey update (přeregistrace zkratky)

#### **base_translator.py** - Abstrakce (93 řádků)
- `BaseTranslator` - abstraktní rozhraní (ABC)
  - `translate()` - hlavní překladová metoda
  - `get_usage()` - získání usage statistik
  - `is_configured()` - kontrola konfigurace
- `UsageInfo` - dataclass pro usage statistiky

#### **deepl_translator.py** / **google_translator.py**
- Implementace `BaseTranslator` pro DeepL / Google
- Error handling + fallback logika
- Google Translate je zdarma (neomezené použití)

#### **config.py** - Konfigurace (124 řádků)
- `Config` - správa nastavení (JSON + .env)
  - `load()` / `save()` - persistentní uložení
  - `set()` / `get()` - getter/setter pro konfiguraci
  - `set_api_key()` - secure storage pro API klíč (.env)

## ⚠️ Známé problémy

- **Globální zkratky**: Na některých systémech může být potřeba administrátorské oprávnění
- **System Tray**: První spuštění může trvat déle kvůli vytvoření ikony

## 🔮 Budoucí rozšíření a příprava

### ✅ Implementováno:
- **Python best practices struktura**: `src/transka/` package layout
- **Console scripts**: `transka` příkaz po instalaci
- **Module execution**: `python -m transka` podpora
- **Architektura pro více překladačů**: BaseTranslator abstrakce
- **Google Translate implementace**: Plně funkční pomocí `googletrans` knihovny
- **Přepínání překladačů**: Výběr v nastavení mezi DeepL a Google
- **Live reload**: Změna překladače se aplikuje okamžitě bez restartu
- **UV package manager**: Moderní instalace a správa závislostí
- **Spouštění bez konzole**: .bat script
- **Dark theme**: Modern cyberpunk design s Fira Code fontem
- **Modulární architektura**: Clean Code s 7 specializovanými moduly
- **State machine workflow**: 3-step překlad proces

### 📋 Plánováno:

#### 🔥 Vysoká priorita (klávesové zkratky):
- [ ] **Přepnutí směru jazyků** - globální zkratka (pravděpodobně Ctrl+S+S)
  - Rychlá změna CS→EN na EN→CS a zpět
  - Bez nutnosti otevírat Settings
- [ ] **Vymazání input pole** - globální zkratka (pravděpodobně Ctrl+C+C)
  - Rychlé vyčištění textu k překladu
  - Alternativa k tlačítku "Vymazat"

#### 🚀 Další features:
- [ ] **Automatické přepnutí na Google Translate** po dosažení 490k znaků DeepL limitu
- [ ] **Historie překladů**: Ukládání posledních N překladů (Ctrl+H+H pro otevření?)
- [ ] **Export/import nastavení**: Backup konfigurace
- [ ] **Autostart s Windows**: Přidání do registry
- [ ] **Systémový installer**: .exe pomocí PyInstaller/cx_Freeze
- [ ] **Rozšíření jazyků**: Podpora všech jazyků z googletrans.LANGUAGES
- [ ] **Automatická detekce jazyka**: Inteligentní swap CS↔EN podle vstupního textu

## 📄 Licence

MIT License

## 👨‍💻 Autor

DeepL Translator App - 2025
