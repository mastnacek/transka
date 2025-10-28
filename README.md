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

1. **Naklonujte repozitář nebo stáhněte soubory**

2. **Vytvořte virtuální prostředí** (doporučeno):
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Nainstalujte závislosti**:
```bash
pip install -r requirements.txt
```

4. **Vytvořte `.env` soubor**:
```bash
copy .env.example .env
```

5. **Vložte DeepL API klíč** do `.env`:
```
DEEPL_API_KEY=your-actual-api-key-here
```

## 🎯 Jak získat DeepL API klíč

1. Navštivte [DeepL API Free](https://www.deepl.com/pro-api)
2. Zaregistrujte se pro Free API (500,000 znaků/měsíc zdarma)
3. Zkopírujte API klíč z dashboardu
4. Vložte do `.env` souboru

## 🏃 Spuštění

```bash
python main.py
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
├── main.py           # Hlavní aplikace (GUI, tray, zkratky)
├── translator.py     # DeepL API komunikace
├── config.py         # Správa konfigurace
├── requirements.txt  # Python závislosti
├── .env             # Konfigurace (API klíč) - gitignored
├── .env.example     # Příklad konfigurace
├── config.json      # Uživatelské nastavení
└── README.md        # Dokumentace
```

## ⚠️ Známé problémy

- **Globální zkratky**: Na některých systémech může být potřeba administrátorské oprávnění
- **System Tray**: První spuštění může trvat déle kvůli vytvoření ikony

## 🔮 Budoucí rozšíření

- [ ] Přepnutí na Google Translate API po dosažení limitu DeepL
- [ ] Historie překladů
- [ ] Podpora více překladačů současně
- [ ] Export/import nastavení

## 📄 Licence

MIT License

## 👨‍💻 Autor

DeepL Translator App - 2025
