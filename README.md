# DeepL Translator - Desktop App

Jednoduchá desktop aplikace pro rychlý překlad pomocí DeepL API s podporou system tray a globálních klávesových zkratek.

## 🚀 Funkce

- **System Tray**: Aplikace běží na pozadí v system tray
- **Jediná klávesová zkratka `Win+P`**:
  - **První stisk**: Otevře překladové okno s fokusem na input
  - **Druhý stisk**: Přeloží text a zkopíruje do schránky + skryje okno
- **Počítadlo znaků**: Sledování spotřeby DeepL API (Free: 500,000 znaků/měsíc)
- **Varování při limitu**: Upozornění při dosažení 96% limitu
- **Jednoduché GUI**: Minimalistické rozhraní s Tkinter
- **Konfigurovatelné**: Nastavení jazyků, API klíče a zkratek

## 📋 Požadavky

- Python 3.8+
- DeepL API klíč (Free nebo Pro)
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
deepl-translator
```

Aplikace se spustí v system tray. Klikněte na ikonu pro otevření menu.

## ⚙️ Nastavení

- **API klíč**: DeepL API klíč (Free nebo Pro)
- **Zdrojový jazyk**: Jazyk vstupního textu (AUTO pro automatickou detekci)
- **Cílový jazyk**: Jazyk překladu
- **Klávesová zkratka**: Přizpůsobení hlavní zkratky Win+P (vyžaduje restart)
- **Práh varování**: Limit znaků pro varování (výchozí: 480,000)

## 🎮 Použití

### Základní workflow:
1. Stiskněte `Win + P` pro otevření okna
2. Vložte text k překladu (okno má automatický fokus)
3. Stiskněte `Win + P` znovu (nebo klikněte na "Přeložit")
4. Překlad se automaticky zkopíruje do schránky
5. Okno se automaticky skryje
6. Vložte překlad kamkoli pomocí `Ctrl + V`

**💡 Tip**: Stačí pamatovat jen `Win + P` - první stisk otevře, druhý přeloží!

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
- **DeepL API**: Překladová služba
- **pystray**: System tray ikona
- **keyboard**: Globální klávesové zkratky
- **pyperclip**: Práce se schránkou

## 📝 Struktura projektu

```
transka/
├── src/
│   └── transka/              # Hlavní package (Python best practice)
│       ├── __init__.py       # Package exports (__all__, __version__)
│       ├── __main__.py       # Entry point pro: python -m transka
│       ├── app.py            # Hlavní aplikace (GUI, tray, zkratky)
│       ├── config.py         # Správa konfigurace
│       ├── base_translator.py    # Abstraktní rozhraní pro překladače
│       ├── deepl_translator.py   # DeepL API implementace
│       ├── google_translator.py  # Google Translate (připraveno)
│       └── translator.py     # Legacy wrapper (deprecated)
├── install.bat               # Instalační script (Windows)
├── start.bat                 # Spouštěcí script (bez konzole)
├── pyproject.toml            # Modern Python package konfigurace
├── requirements.txt          # Python závislosti (pip fallback)
├── .env                      # Konfigurace (API klíč) - gitignored
├── .env.example              # Příklad konfigurace
├── config.json               # Uživatelské nastavení - gitignored
└── README.md                 # Dokumentace
```

## ⚠️ Známé problémy

- **Globální zkratky**: Na některých systémech může být potřeba administrátorské oprávnění
- **System Tray**: První spuštění může trvat déle kvůli vytvoření ikony

## 🔮 Budoucí rozšíření a příprava

### ✅ Připraveno (implementováno):
- **Python best practices struktura**: `src/transka/` package layout
- **Console scripts**: `deepl-translator` příkaz po instalaci
- **Module execution**: `python -m transka` podpora
- **Architektura pro více překladačů**: BaseTranslator abstrakce
- **Google Translate placeholder**: Připraveno pro budoucí implementaci
- **UV package manager**: Moderní instalace a správa závislostí
- **Spouštění bez konzole**: .bat script

### 📋 Plánováno:
- [ ] **Automatické přepnutí na Google Translate** po dosažení 490k znaků DeepL limitu
- [ ] **Google Translate implementace**: Dokončení google_translator.py
- [ ] **Historie překladů**: Ukládání posledních N překladů
- [ ] **Podpora více překladačů současně**: Výběr v nastavení
- [ ] **Export/import nastavení**: Backup konfigurace
- [ ] **Autostart s Windows**: Přidání do registry
- [ ] **Systémový installer**: .exe pomocí PyInstaller/cx_Freeze

## 📄 Licence

MIT License

## 👨‍💻 Autor

DeepL Translator App - 2025
