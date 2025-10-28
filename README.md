# DeepL Translator - Desktop App

Jednoduchá desktop aplikace pro rychlý překlad pomocí DeepL API s podporou system tray a globálních klávesových zkratek.

## 🚀 Funkce

- **System Tray**: Aplikace běží na pozadí v system tray
- **Globální klávesové zkratky**:
  - `Win + Mezerník`: Otevře překladové okno
  - `Win + P`: Přeloží text a zkopíruje do schránky
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
```powershell
# PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

2. **Spusťte instalační script**:
```bash
# PowerShell
.\install.ps1

# Nebo CMD
install.bat
```

3. **Nastavte DeepL API klíč** v `.env` souboru:
```
DEEPL_API_KEY=your-actual-api-key-here
```

4. **Spusťte aplikaci**:
```bash
# PowerShell (bez konzole)
.\start.ps1

# Nebo CMD
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
pythonw -m src.main

# S konzolí (pro debugging)
python -m src.main
```

## 🎯 Jak získat DeepL API klíč

1. Navštivte [DeepL API Free](https://www.deepl.com/pro-api)
2. Zaregistrujte se pro Free API (500,000 znaků/měsíc zdarma)
3. Zkopírujte API klíč z dashboardu
4. Vložte do `.env` souboru

## 🏃 Spuštění

### Pomocí UV:
```bash
# PowerShell (bez konzole)
.\start.ps1

# CMD
start.bat
```

### Klasicky:
```bash
# Bez konzole (doporučeno - aplikace běží na pozadí)
pythonw -m src.main

# S konzolí (pro debugging)
python -m src.main
```

Aplikace se spustí v system tray. Klikněte na ikonu pro otevření menu.

## ⚙️ Nastavení

- **API klíč**: DeepL API klíč (Free nebo Pro)
- **Zdrojový jazyk**: Jazyk vstupního textu (AUTO pro automatickou detekci)
- **Cílový jazyk**: Jazyk překladu
- **Klávesové zkratky**: Přizpůsobení zkratek (vyžaduje restart)
- **Práh varování**: Limit znaků pro varování (výchozí: 480,000)

## 🎮 Použití

### Základní workflow:
1. Stiskněte `Win + Mezerník` pro otevření okna
2. Vložte text k překladu
3. Stiskněte `Win + P` nebo klikněte na "Přeložit"
4. Překlad se zkopíruje do schránky
5. Okno se automaticky skryje
6. Vložte překlad kamkoli pomocí `Ctrl + V`

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
│   ├── __init__.py           # Package inicializace
│   ├── main.py               # Hlavní aplikace (GUI, tray, zkratky)
│   ├── config.py             # Správa konfigurace
│   ├── base_translator.py    # Abstraktní rozhraní pro překladače
│   ├── deepl_translator.py   # DeepL API implementace
│   ├── google_translator.py  # Google Translate (připraveno)
│   └── translator.py         # Legacy wrapper (deprecated)
├── install.bat               # Instalační script (Windows CMD)
├── install.ps1               # Instalační script (PowerShell)
├── start.bat                 # Spouštěcí script (CMD, bez konzole)
├── start.ps1                 # Spouštěcí script (PowerShell, bez konzole)
├── pyproject.toml            # UV/pip konfigurace
├── requirements.txt          # Python závislosti (pip)
├── .env                      # Konfigurace (API klíč) - gitignored
├── .env.example              # Příklad konfigurace
├── config.json               # Uživatelské nastavení - gitignored
└── README.md                 # Dokumentace
```

## ⚠️ Známé problémy

- **Globální zkratky**: Na některých systémech může být potřeba administrátorské oprávnění
- **System Tray**: První spuštění může trvat déle kvůli vytvoření ikony

## 🔮 Budoucí rozšíření a příprava

### Připraveno (abstrakce implementována):
- ✅ **Architektura pro více překladačů**: BaseTranslator abstrakce
- ✅ **Google Translate placeholder**: Připraveno pro budoucí implementaci
- ✅ **UV package manager**: Moderní instalace a správa závislostí
- ✅ **Spouštění bez konzole**: .bat a .ps1 scripty

### Plánováno:
- [ ] **Automatické přepnutí na Google Translate** po dosažení 490k znaků DeepL limitu
- [ ] **Google Translate implementace**: Dokončení google_translator.py
- [ ] **Historie překladů**: Ukládání posledních N překladů
- [ ] **Podpora více překladačů současně**: Výběr v nastavení
- [ ] **Export/import nastavení**: Backup konfigurace
- [ ] **Autostart s Windows**: Přidání do registry

## 📄 Licence

MIT License

## 👨‍💻 Autor

DeepL Translator App - 2025
