# GUI Redesign - Analýza a Implementační Plán

**Projekt:** Transka Desktop Translator
**Cíl:** Přesun Settings z popup okna do tab-based interface v hlavním okně
**Datum:** 2025-01-29
**Analýza:** ULTRATHINK Deep Analysis

---

## 📊 Executive Summary

**Současný stav:** Settings jsou v separátním popup okně (`SettingsWindow`)
**Navržená změna:** Integrace Settings do hlavního okna pomocí ttk.Notebook (tabs)
**Dopad:** ✅ Lepší UX, ✅ Modernější vzhled, ✅ Rychlejší přístup k nastavení
**Časová náročnost:** 3-5 dní (včetně testování)
**Riziko:** 🟡 Střední (breaking changes v GUI architektuře)

---

## 🔍 1. ANALÝZA SOUČASNÉHO STAVU

### Současná architektura

```
src/transka/
├── gui_builder.py (245 řádků)
│   └── GUIBuilder class
│       ├── Header (překladač + jazyky)
│       ├── Input field (8 rows)
│       ├── Output field (8 rows)
│       ├── Status bar (usage + status)
│       └── Buttons: [Přeložit] [Vymazat] [Nastavení] [Zavřít]
│
└── settings_window.py (235 řádků)
    └── SettingsWindow class (Toplevel popup)
        ├── Překladač (DeepL/Google)
        ├── API klíč (show="*")
        ├── Zdrojový jazyk (CS/EN/DE/...)
        ├── Cílový jazyk (CS/EN-US/EN-GB/...)
        ├── Hlavní zkratka (ctrl+p)
        ├── Swap zkratka (ctrl+s)
        ├── Clear zkratka (ctrl+c)
        ├── Varování threshold (480000)
        └── Buttons: [Uložit] [Test API] [Zrušit]
```

### Současný User Flow

```
1. User otevře aplikaci (Ctrl+P+P)
2. Napíše text → přeloží (Ctrl+P+P)
3. Potřebuje změnit nastavení:
   ❌ Click "Nastavení" → popup okno
   ❌ Změní settings
   ❌ Click "Uložit"
   ❌ Popup zavře
4. Vrátí se k překladu
```

### Problémy současného řešení

| Problém | Popis | Dopad |
|---------|-------|-------|
| **Přerušení workflow** | Popup okno zakryje hlavní okno | Uživatel ztrácí kontext |
| **Nekonzistence** | Některé akce globální (Ctrl+S+S), jiné vyžadují popup | Matoucí UX |
| **Skrytá funkcionalita** | Settings viditelné až po otevření popup | Nižší discovera​bility |
| **Zbytečné kroky** | Open → Edit → Save → Close = 4 akce | Pomalý workflow |
| **Rigidní layout** | Fixed 500x590 popup, neresizable | Omezená flexibilita |

---

## 📚 2. BEST PRACTICES Z VÝZKUMU

### UI/UX Best Practices (zdroj: NN/Group, LogRocket, UX Planet 2024-2025)

#### Kdy použít tabs v settings panelech

✅ **ANO - Použít tabs když:**
- Máte 2-7 kategorií nastavení
- Každá kategorie je logicky oddělená
- Uživatel nepotřebuje vidět vše najednou
- Chcete redukovat cognitive load
- Moderní, clean interface

❌ **NE - Nepoužívat tabs když:**
- Máte pouze 1-2 nastavení (zbytečné)
- Uživatel potřebuje vidět všechny hodnoty současně
- Častá navigace mezi tabs (> 5x za session)

**Náš případ:** ✅ **POUŽÍT TABS** - 8 nastavení, logicky oddělitelné (Translation vs Settings)

#### Visual Design Guidelines

**Active State Indicators:**
```python
# Border thickness pro active tab
active_border: 2-4px
inactive_border: 1px

# Elevation
active_tab: elevation +2px
inactive_tab: flat

# Color contrast
active_bg: Same as content panel background
inactive_bg: Slightly darker/lighter
```

**Animation & Transitions:**
- Duration: **< 300ms** (prevent lag perception)
- Type: Slide + fade (spatial awareness)
- Figma example: 250ms optimal

**Typography:**
```
Tab label:
  - Active: Bold, 14px
  - Inactive: Regular, 14px
  - Color difference: High contrast (WCAG AA)
```

#### Accessibility (ARIA & Keyboard)

```html
<!-- Role assignment -->
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel1">Překlad</button>
  <button role="tab" aria-selected="false" aria-controls="panel2">Nastavení</button>
</div>
<div role="tabpanel" id="panel1" aria-labelledby="tab1">...</div>

<!-- Keyboard support -->
Tab: Navigate between tabs
Enter/Space: Activate tab
Ctrl+Tab: Next tab (optional)
```

**Python Tkinter ekvivalent:**
```python
# Focus ring pro keyboard navigation
tab_button.config(highlightthickness=2, highlightcolor="cyan")

# Keyboard bindings
root.bind("<Control-1>", lambda e: notebook.select(0))  # Ctrl+1 = První tab
root.bind("<Control-2>", lambda e: notebook.select(1))  # Ctrl+2 = Druhý tab
```

#### Nesting Limit

**Maximum 2 levels** of tab nesting:
```
Good:
  Level 1: [Překlad] [Nastavení]
  Level 2: [Překladač] [Hotkeys] (inside Nastavení)

Bad:
  Level 3+: Too deep, use accordions/panels instead
```

**Náš případ:** 1 level (Překlad + Nastavení) = ✅ Optimální

---

### Tkinter ttk.Notebook Best Practices

#### Základní použití

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")

# Event handling
def on_tab_changed(event):
    current = notebook.index(notebook.select())
    print(f"Switched to tab {current}")

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
```

#### Styling (Dark Theme)

```python
style = ttk.Style()

# Tab styling
style.configure("TNotebook",
    background="#1a1a2e",  # Dark bg
    borderwidth=0
)

style.configure("TNotebook.Tab",
    background="#2d2d44",      # Inactive tab
    foreground="#a0a0c0",      # Inactive text
    padding=[20, 10],          # Horizontal, vertical
    font=("Segoe UI", 10)
)

style.map("TNotebook.Tab",
    background=[("selected", "#1a1a2e")],  # Active tab = same as content
    foreground=[("selected", "#00d9ff")],   # Active text = cyan accent
    expand=[("selected", [1, 1, 1, 0])]     # Expand active tab
)
```

#### Programmatic Tab Control

```python
# Get current tab
current = notebook.index(notebook.select())

# Switch to specific tab
notebook.select(0)  # First tab (Překlad)
notebook.select(1)  # Second tab (Nastavení)

# Hide/show tabs dynamically
notebook.hide(1)  # Hide Settings tab
notebook.add(settings_tab, text="Nastavení")  # Show again

# Get tab count
count = notebook.index("end")
```

---

## 🎨 3. NÁVRH NOVÉ ARCHITEKTURY

### Varianta A: Dvoutabové rozhraní (DOPORUČENO)

#### Mockup

```
┌──────────────────────────────────────────────────────────┐
│ Transka                                          [–][□][X]│
├──────────────────────────────────────────────────────────┤
│ 🟢 DeepL | 🌐 CS → EN-US                                 │ ← Header (global)
├──────────────────────────────────────────────────────────┤
│ ┌────────────┐┌──────────────┐                           │
│ │  Překlad   ││  Nastavení   │                           │ ← Tabs
│ └────────────┘└──────────────┘                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ TAB 1: PŘEKLAD (current: gui_builder.py content)         │
│ ┌───────────────────────────────────────────────────────┐│
│ │ Text k překladu:                                      ││
│ │ ┌───────────────────────────────────────────────────┐ ││
│ │ │                                                   │ ││
│ │ │                                                   │ ││
│ │ │                   (8 rows)                        │ ││
│ │ │                                                   │ ││
│ │ │                                                   │ ││
│ │ └───────────────────────────────────────────────────┘ ││
│ │                                                       ││
│ │ Přeložený text:                                       ││
│ │ ┌───────────────────────────────────────────────────┐ ││
│ │ │                                                   │ ││
│ │ │                                                   │ ││
│ │ │                   (8 rows)                        │ ││
│ │ │                                                   │ ││
│ │ │                                                   │ ││
│ │ └───────────────────────────────────────────────────┘ ││
│ │                                                       ││
│ │ Status: Připraveno        │ Usage: 15,234 / 500,000  ││
│ │                                                       ││
│ │ [Přeložit (Ctrl+Enter)] [Vymazat]                    ││
│ └───────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

```
TAB 2: NASTAVENÍ (current: settings_window.py → tab frame)
┌──────────────────────────────────────────────────────────┐
│ ┌───────────────────────────────────────────────────────┐│
│ │ Překladač:                                            ││
│ │ [DeepL                    ▼]                          ││
│ │                                                       ││
│ │ DeepL API klíč:                                       ││
│ │ [●●●●●●●●●●●●●●●●●●●●●●●●]  [Test API]                ││
│ │                                                       ││
│ │ Zdrojový jazyk:                                       ││
│ │ [CS                       ▼]                          ││
│ │                                                       ││
│ │ Cílový jazyk:                                         ││
│ │ [EN-US                    ▼]                          ││
│ │                                                       ││
│ │ ──── Klávesové zkratky ────                           ││
│ │                                                       ││
│ │ Hlavní zkratka:                                       ││
│ │ [ctrl+p          ]  (Ctrl+P+P double-press)          ││
│ │                                                       ││
│ │ Swap jazyků:                                          ││
│ │ [ctrl+s          ]  (Ctrl+S+S double-press)          ││
│ │                                                       ││
│ │ Vymazat input:                                        ││
│ │ [ctrl+c          ]  (Ctrl+C+C double-press)          ││
│ │                                                       ││
│ │ Varování při (znacích):                               ││
│ │ [480000          ]                                    ││
│ │                                                       ││
│ │                      [Uložit]                         ││
│ └───────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

#### Výhody této varianty

| Výhoda | Popis | Měřitelný dopad |
|--------|-------|-----------------|
| **Vše na jednom místě** | Žádné popup okno | -2 clicks (Open + Close popup) |
| **Rychlé přepínání** | 1 click pro přístup k settings | -3 clicks vs popup workflow |
| **Live preview** | Vidíte aktuální nastavení v headeru | Lepší awareness |
| **Konzistence** | Podobné moderním aplikacím (VS Code, Spotify) | Higher familiarity |
| **Accessibility** | Keyboard navigation (Tab, Ctrl+1/2) | WCAG AA compliant |
| **Méně kódu** | Jeden builder místo dvou | -50 řádků kódu (odhad) |
| **Flexibilita** | Lze přidat třetí tab (Historie) | Future-proof |

#### Nevýhody a mitigace

| Nevýhoda | Mitigace |
|----------|----------|
| Větší hlavní okno (700x550 vs 600x400) | Dynamický resize nebo uživatel si zvykne |
| Ztráta "Save/Cancel" workflow | Ponechat [Uložit] tlačítko v Settings tab |
| Možná složitější kód | Dobře strukturovaný GUIBuilderV2 to vyřeší |

---

### Varianta B: Tříta​bové rozhraní (Budoucnost)

```
┌────────────┐┌──────────────┐┌──────────────┐
│  Překlad   ││  Nastavení   ││   Historie   │
└────────────┘└──────────────┘└──────────────┘
                                    ↑
                              Future feature
```

**Přidaná hodnota:**
- Historie překladů (Ctrl+H+H)
- Export/import překladů
- Statistiky (počet překladů, nejpoužívanější jazyky)

**Implementace:** Po dokončení Varianty A

---

### Varianta C: Collapsible Panel (Accordion) - NEDOPORUČENO

```
┌─────────────────────────────────┐
│ Input pole                       │
│ Output pole                      │
│ [Přeložit] [Vymazat]            │
│                                  │
│ ┌─ [▼ Pokročilé nastavení] ────┐│
│ │ Překladač: [DeepL ▼]         ││
│ │ API klíč:  [●●●●●●]          ││
│ │ ...                           ││
│ └──────────────────────────────┘│
└─────────────────────────────────┘
```

**Proč NE:**
- ❌ Skrytá funkcionalita (hidden by default)
- ❌ Vertikální scroll při rozbalení
- ❌ Méně intuitivní než tabs

---

### Varianta D: Sidebar - NEDOPORUČENO

```
┌────┬───────────────┐
│ ⚙  │ Input pole    │
│ 🌐 │ Output pole   │
│ 🎨 │               │
│    │               │
└────┴───────────────┘
```

**Proč NE:**
- ❌ Zabírá horizontální prostor (menší input/output)
- ❌ Nevhodné pro desktop app (lepší pro web)
- ❌ Komplikované na malých obrazovkách

---

## 🏗️ 4. IMPLEMENTAČNÍ PLÁN

### Fáze 1: Příprava (1 den)

#### Úkoly

- [ ] Backup současného kódu
  ```bash
  git commit -m "🔖 snapshot: Backup před GUI redesign"
  ```

- [ ] Vytvořit novou větev
  ```bash
  git checkout -b feature/gui-tabs-redesign
  ```

- [ ] Vytvořit `gui_builder_v2.py` (kopie gui_builder.py)
  ```bash
  cp src/transka/gui_builder.py src/transka/gui_builder_v2.py
  ```

- [ ] Prostudovat ttk.Notebook API
  - Přečíst: https://www.pythontutorial.net/tkinter/tkinter-notebook/
  - Experimentovat: Vytvořit POC (proof of concept) s 2 tabs

#### Deliverables

- ✅ Git snapshot
- ✅ Nová větev `feature/gui-tabs-redesign`
- ✅ `gui_builder_v2.py` připraven
- ✅ POC funkční (2 dummy tabs)

---

### Fáze 2: Refactoring GUIBuilder (2 dny)

#### Úkol 1: Vytvoření ttk.Notebook struktury

**Soubor:** `src/transka/gui_builder_v2.py`

```python
class GUIBuilderV2:
    """Builder pro GUI s tab-based interface"""

    def __init__(self, root, fonts, translator_display, language_display):
        self.root = root
        self.fonts = fonts
        self.translator_display = translator_display
        self.language_display = language_display

        # Notebook (tabs)
        self.notebook = None

        # Tab frames
        self.translation_tab = None
        self.settings_tab = None

        # Widgets (z obou tabs)
        self.input_text = None
        self.output_text = None
        self.status_label = None
        self.usage_label = None
        # ... settings widgets ...

    def build(self, on_translate, on_clear, on_save_settings, on_test_api):
        """Vytvoří kompletní GUI s tabs"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header (global - outside tabs)
        self._create_header(main_frame)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create tabs
        self.translation_tab = self._create_translation_tab(on_translate, on_clear)
        self.settings_tab = self._create_settings_tab(on_save_settings, on_test_api)

        # Add tabs to notebook
        self.notebook.add(self.translation_tab, text=" Překlad ")
        self.notebook.add(self.settings_tab, text=" Nastavení ")

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        return {
            "input_text": self.input_text,
            "output_text": self.output_text,
            "status_label": self.status_label,
            "usage_label": self.usage_label,
            # ... settings widgets ...
        }
```

#### Úkol 2: Translation Tab (přesun z gui_builder.py)

```python
def _create_translation_tab(self, on_translate, on_clear):
    """Vytvoří tab pro překlad (současný obsah gui_builder.py)"""
    frame = ttk.Frame(self.notebook)

    # Konfigurace grid
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)

    # Input pole
    self._create_input_field(frame)

    # Output pole
    self._create_output_field(frame)

    # Status bar
    self._create_status_bar(frame)

    # Tlačítka (pouze Přeložit + Vymazat)
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=4, column=0, pady=(10, 0))

    ttk.Button(button_frame, text="Přeložit (Ctrl+Enter)", command=on_translate).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Vymazat", command=on_clear).pack(side=tk.LEFT, padx=5)

    return frame
```

#### Úkol 3: Settings Tab (přesun z settings_window.py)

```python
def _create_settings_tab(self, on_save, on_test_api):
    """Vytvoří tab pro nastavení (settings_window.py → tab)"""
    frame = ttk.Frame(self.notebook, padding="10")

    # Scrollable frame (pokud settings přeteče)
    canvas = tk.Canvas(frame, bg=COLORS["bg_dark"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid layout
    canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Settings widgets (copy from settings_window.py)
    # ... (all settings fields) ...

    # Tlačítka
    button_frame = ttk.Frame(scrollable_frame)
    button_frame.grid(row=10, column=0, columnspan=2, pady=20)

    ttk.Button(button_frame, text="Uložit", command=on_save).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Test API", command=on_test_api).pack(side=tk.LEFT, padx=5)

    return frame
```

#### Úkol 4: Tab Change Handler

```python
def _on_tab_changed(self, event):
    """Handler pro změnu tabu"""
    current_tab = self.notebook.index(self.notebook.select())

    if current_tab == 0:  # Translation tab
        # Focus na input pole
        self.input_text.focus()
    elif current_tab == 1:  # Settings tab
        # Focus na první settings field
        # (optional - lze nechat bez focus)
        pass
```

#### Deliverables

- ✅ `gui_builder_v2.py` funkční s 2 tabs
- ✅ Translation tab = současný gui_builder obsah
- ✅ Settings tab = současný settings_window obsah
- ✅ Tab switching funguje
- ✅ Keyboard navigation (Tab key)

---

### Fáze 3: Integrace do app.py (1 den)

#### Změny v app.py

```python
# PŘED (současný stav)
from transka.gui_builder import GUIBuilder
from transka.settings_window import SettingsWindow

# PO (nový stav)
from transka.gui_builder_v2 import GUIBuilderV2

class TranslatorApp:
    def __init__(self):
        # ...

        # PŘED
        gui_builder = GUIBuilder(...)
        widgets = gui_builder.build(
            on_translate=self._translate,
            on_clear=self._clear,
            on_settings=self._show_settings,  # ← POPUP
            on_close=self._hide_window
        )

        # PO
        gui_builder = GUIBuilderV2(...)
        widgets = gui_builder.build(
            on_translate=self._translate,
            on_clear=self._clear,
            on_save_settings=self._save_settings,  # ← TAB
            on_test_api=self._test_api             # ← TAB
        )

    # SMAZAT
    def _show_settings(self):
        """Zobrazí popup okno s nastavením"""
        SettingsWindow(...)  # ← DELETE

    # PŘIDAT
    def _save_settings(self):
        """Uloží nastavení z Settings tab"""
        # Logic from settings_window.py::_save_settings()
        pass

    def _test_api(self):
        """Test API z Settings tab"""
        # Logic from settings_window.py::_test_api()
        pass
```

#### Keyboard Shortcuts Update

```python
def _setup_window_events(self):
    """Nastaví události okna"""
    self.root.protocol("WM_DELETE_WINDOW", self._hide_window)
    self.root.bind("<Escape>", lambda e: self._hide_window())
    self.root.bind("<Control-Return>", lambda e: self._translate())

    # NOVÉ - tab switching
    self.root.bind("<Control-Key-1>", lambda e: self._switch_to_translation_tab())
    self.root.bind("<Control-Key-2>", lambda e: self._switch_to_settings_tab())

def _switch_to_translation_tab(self):
    """Přepne na Translation tab (Ctrl+1)"""
    self.gui_builder.notebook.select(0)

def _switch_to_settings_tab(self):
    """Přepne na Settings tab (Ctrl+2)"""
    self.gui_builder.notebook.select(1)
```

#### Workflow Fix - Ctrl+P+P vždy otevře Translation tab

```python
def _handle_main_hotkey(self):
    """Zpracuje hlavní klávesovou zkratku (Ctrl+P+P)"""
    state = self.workflow.get_state()

    if state == TranslationWorkflow.STATE_HIDDEN:
        # NOVÉ - vždy otevřít na Translation tab
        self._show_window()
        self.gui_builder.notebook.select(0)  # ← Force Translation tab
        self.workflow.set_state(TranslationWorkflow.STATE_SHOWN)
    # ... rest stejné ...
```

#### Deliverables

- ✅ `app.py` používá `GUIBuilderV2`
- ✅ `SettingsWindow` import smazán
- ✅ Keyboard shortcuts (Ctrl+1/2) fungují
- ✅ Ctrl+P+P vždy otevře Translation tab

---

### Fáze 4: Styling & Dark Theme (1 den)

#### ttk.Style konfigurace

**Soubor:** `src/transka/theme_manager.py`

```python
def _configure_ttk_styles(self):
    """Konfiguruje TTK styles pro dark theme"""
    style = ttk.Style()

    # ... existing styles ...

    # NOVÉ - Notebook styling
    style.configure("TNotebook",
        background=COLORS["bg_dark"],
        borderwidth=0,
        tabmargins=[0, 0, 0, 0]
    )

    style.configure("TNotebook.Tab",
        background=COLORS["bg_darker"],     # Inactive tab
        foreground=COLORS["text_secondary"], # Inactive text
        padding=[20, 10],                    # Horizontal, vertical
        font=("Segoe UI", 10, "normal"),
        borderwidth=0
    )

    style.map("TNotebook.Tab",
        background=[
            ("selected", COLORS["bg_dark"]),     # Active tab = same as content
            ("active", COLORS["bg_input"])       # Hover
        ],
        foreground=[
            ("selected", COLORS["accent_cyan"]),  # Active text = cyan
            ("active", COLORS["text_primary"])    # Hover text
        ],
        expand=[("selected", [1, 1, 1, 0])]      # Expand to bottom
    )
```

#### Tab Border/Indicator (custom styling)

```python
# V GUIBuilderV2.__init__()
def _style_notebook_tabs(self):
    """Custom styling pro tab indicators"""
    # Active tab indicator (underline)
    style = ttk.Style()
    style.layout("TNotebook.Tab", [
        ("Notebook.tab", {
            "sticky": "nswe",
            "children": [
                ("Notebook.padding", {
                    "side": "top",
                    "sticky": "nswe",
                    "children": [
                        ("Notebook.focus", {
                            "side": "top",
                            "sticky": "nswe",
                            "children": [
                                ("Notebook.label", {"side": "left", "sticky": ""})
                            ]
                        })
                    ]
                })
            ]
        })
    ])
```

#### Window Size Adjustment

```python
# V app.py __init__()
# PŘED
self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")  # 600x400

# PO
self.root.geometry("700x550")  # Větší okno pro tabs

# NEBO dynamický resize podle tabu
def _on_tab_changed(self, event):
    current = self.notebook.index(self.notebook.select())
    if current == 0:  # Translation
        self.root.geometry("700x500")
    elif current == 1:  # Settings
        self.root.geometry("700x550")
```

#### Deliverables

- ✅ Dark theme pro tabs
- ✅ Active tab indicator (underline/border)
- ✅ Hover effects
- ✅ Window size optimalizován
- ✅ Konzistentní s ostatními widgety

---

### Fáze 5: Testing & Polish (1 den)

#### Test Cases

| Test Case | Popis | Očekávaný výsledek |
|-----------|-------|-------------------|
| **TC1: Tab Switching** | Click na Nastavení tab | Settings tab se zobrazí, input pole mizí |
| **TC2: Keyboard Nav** | Ctrl+1 → Ctrl+2 → Ctrl+1 | Tabs se přepínají správně |
| **TC3: Tab Focus** | Ctrl+P+P otevře okno | Vždy otevře Translation tab |
| **TC4: Settings Save** | Změna API klíče → Uložit | Live reload, header update |
| **TC5: Tab Persistence** | Zavřít okno v Settings tab → otevřít Ctrl+P+P | Otevře Translation tab (ne Settings) |
| **TC6: Scroll Settings** | Dlouhý seznam settings | Scrollbar funguje |
| **TC7: Dark Theme** | Visual check všech tabs | Konzistentní styling |
| **TC8: Accessibility** | Tab navigation pomocí klávesnice | Focus ring viditelný |

#### Manual Testing Checklist

- [ ] Translation tab: Input + Output funguje
- [ ] Translation tab: Přeložit tlačítko funguje
- [ ] Translation tab: Vymazat tlačítko funguje
- [ ] Translation tab: Status bar update
- [ ] Settings tab: Všechny fields editovatelné
- [ ] Settings tab: Uložit aplikuje změny
- [ ] Settings tab: Test API funguje
- [ ] Settings tab: Scroll funguje (pokud přetéká)
- [ ] Tab switching: Click funguje
- [ ] Tab switching: Ctrl+1/2 funguje
- [ ] Dark theme: Konzistentní barvy
- [ ] Dark theme: Active tab viditelný
- [ ] Window resize: Velikost optimální
- [ ] Ctrl+P+P workflow: Vždy Translation tab

#### Deliverables

- ✅ Všechny test cases passed
- ✅ Manual testing checklist completed
- ✅ Bug fixes (pokud nějaké)
- ✅ Screenshot nového GUI (pro dokumentaci)

---

### Fáze 6: Cleanup & Documentation (půl dne)

#### Code Cleanup

- [ ] Smazat `src/transka/settings_window.py`
  ```bash
  git rm src/transka/settings_window.py
  ```

- [ ] Přejmenovat `gui_builder_v2.py` → `gui_builder.py`
  ```bash
  git mv src/transka/gui_builder_v2.py src/transka/gui_builder.py
  ```

- [ ] Update imports v `app.py`
  ```python
  # FROM
  from transka.gui_builder_v2 import GUIBuilderV2

  # TO
  from transka.gui_builder import GUIBuilder
  ```

- [ ] Smazat nepoužívané metody v `app.py`
  - `_show_settings()` popup metoda
  - Zbylé reference na `SettingsWindow`

#### Documentation Updates

**CLAUDE.md:**
```markdown
## 📝 Architektura projektu

### GUI Layer:
- `gui_builder.py` (300+ řádků) ⭐ TAB-BASED INTERFACE
  - GUIBuilder - Builder pattern pro vytvoření widgets
  - Tab 1: Translation (input/output fields)
  - Tab 2: Settings (všechna nastavení)
  - ttk.Notebook pro tab management
  - Callback injection pro event handling
```

**README.md:**
```markdown
## 🎮 Použití

### Přepínání mezi Překlad a Nastavení

**Tabs v hlavním okně:**
- **Tab "Překlad"**: Překladové pole (input/output)
  - Klávesová zkratka: `Ctrl+1`
- **Tab "Nastavení"**: Všechna nastavení aplikace
  - Klávesová zkratka: `Ctrl+2`

**Workflow:**
1. Ctrl+P+P → Otevře okno na tab Překlad
2. Ctrl+2 → Přepne na tab Nastavení
3. Změna nastavení → Uložit
4. Ctrl+1 → Zpět na tab Překlad
```

#### Git Workflow

```bash
# Review changes
git diff

# Commit refactoring
git add .
git commit -m "♻️ refactor: Redesign GUI - Settings do tabs (ttk.Notebook)

Změny:
- Přesun Settings z popup okna do tabu v hlavním okně
- Implementace ttk.Notebook s 2 tabs (Překlad + Nastavení)
- Smazání settings_window.py
- Refactoring gui_builder.py → tab-based architecture
- Keyboard shortcuts: Ctrl+1 (Překlad), Ctrl+2 (Nastavení)
- Dark theme styling pro tabs
- Window size: 700x550 (optimalizováno pro tabs)

UX improvements:
- Vše na jednom místě - žádné popup okno
- Rychlejší přístup k nastavení (1 click místo popup workflow)
- Modernější vzhled (konzistentní s VS Code, Spotify)
- Lepší accessibility (keyboard navigation)

Breaking changes:
- SettingsWindow class odstraněna
- GUIBuilder API změněno (nové callbacks)

🔗 Implementuje: gui.md plán
"

# Merge do main
git checkout master
git merge feature/gui-tabs-redesign

# Push
git push origin master
```

#### Deliverables

- ✅ `settings_window.py` smazán
- ✅ `gui_builder_v2.py` → `gui_builder.py`
- ✅ Dokumentace aktualizována (CLAUDE.md, README.md)
- ✅ Git commit vytvořen
- ✅ Změny pushnuty

---

## ⚠️ 5. RIZIKA A MITIGACE

### Riziko 1: Breaking Changes v GUI architektuře

**Popis:**
Změna z popup okna na tabs = velká změna v `app.py` a `gui_builder.py`

**Pravděpodobnost:** 🟡 Střední
**Dopad:** 🔴 Vysoký (aplikace může přestat fungovat)

**Mitigace:**
1. Git branch `feature/gui-tabs-redesign` - testování izolované
2. Incremental testing - testovat po každé fázi
3. Rollback plán - `git checkout master` pokud selže

---

### Riziko 2: Workflow Disruption (Ctrl+P+P)

**Popis:**
Co když user otevře okno Ctrl+P+P, ale je v Settings tab? Měl by se přepnout na Translation?

**Pravděpodobnost:** 🟢 Nízká
**Dopad:** 🟡 Střední (matoucí UX)

**Řešení:**
```python
def _handle_main_hotkey(self):
    if state == TranslationWorkflow.STATE_HIDDEN:
        self._show_window()
        self.gui_builder.notebook.select(0)  # ← VŽDY Translation tab
```

**Alternativa:**
Pamatovat si poslední aktivní tab a otevřít na něm → ❌ Matoucí, Ctrl+P je pro překlad

---

### Riziko 3: Window Size - příliš velké?

**Popis:**
Zvětšení okna z 600x400 na 700x550 může být příliš velké na malých monitorech.

**Pravděpodobnost:** 🟡 Střední
**Dopad:** 🟢 Nízký (pouze vizuální)

**Řešení A: Dynamický resize podle tabu**
```python
def _on_tab_changed(self, event):
    current = self.notebook.index(self.notebook.select())
    if current == 0:  # Translation
        self.root.geometry("600x400")  # Původní velikost
    elif current == 1:  # Settings
        self.root.geometry("700x550")  # Větší pro settings
```

**Řešení B: Scrollable Settings tab**
```python
# Pokud settings přetéká, přidat scrollbar
canvas = tk.Canvas(settings_frame)
scrollbar = ttk.Scrollbar(settings_frame, command=canvas.yview)
```

**Doporučení:** Řešení B (scrollable) - konzistentnější UX

---

### Riziko 4: Live Reload vs Uložit tlačítko

**Popis:**
Současně: [Uložit] tlačítko potvrzuje změny.
Po redesignu: Ponechat [Uložit] nebo auto-save?

**Pravděpodobnost:** 🟡 Střední
**Dopad:** 🟡 Střední (user může omylem změnit settings)

**Řešení A: Ponechat [Uložit] tlačítko**
- ✅ Bezpečné - user musí potvrdit
- ✅ Konzistentní se současným workflow
- ❌ Extra krok

**Řešení B: Auto-save s Undo**
- ✅ Rychlejší workflow
- ❌ Složitější implementace (Undo stack)
- ❌ Rizikovější (omylem změnit)

**Doporučení:** Řešení A - **ponechat [Uložit] tlačítko**

---

### Riziko 5: Keyboard Navigation - Accessibility

**Popis:**
Tabs musí být přístupné pomocí klávesnice (WCAG AA).

**Pravděpodobnost:** 🟢 Nízká
**Dopad:** 🟡 Střední (accessibility issue)

**Řešení:**
```python
# Tab key navigace mezi widgety
# Ctrl+Tab / Ctrl+Shift+Tab navigace mezi tabs (optional)
# Ctrl+1/2 direct tab selection

# Focus ring
style.map("TNotebook.Tab",
    background=[("focus", COLORS["accent_cyan"])],
    borderwidth=[("focus", 2)]
)
```

**Testing:**
- [ ] Tab key přepíná mezi widgety
- [ ] Ctrl+1/2 přepíná tabs
- [ ] Focus ring viditelný

---

## 📊 6. DOPORUČENÍ A ROZHODNUTÍ

### Finální doporučení: **VARIANTA A - DVOUTABOVÉ ROZHRANÍ**

#### Proč tato varianta?

| Kritérium | Score | Vysvětlení |
|-----------|-------|------------|
| **UX Improvement** | 9/10 | Vše na jednom místě, rychlejší workflow |
| **Modern Look** | 10/10 | Tabs = industry standard (VS Code, Spotify, atd.) |
| **Maintainability** | 8/10 | Méně souborů, konzistentnější kód |
| **Accessibility** | 9/10 | Keyboard navigation, WCAG AA |
| **Future-proof** | 10/10 | Lze přidat třetí tab (Historie) |
| **Implementation Risk** | 6/10 | Střední riziko, ale mitigovatelné |
| **Time Investment** | 7/10 | 3-5 dní, ale long-term gain |

**Celkový score:** 8.4/10 → ✅ **SILNĚ DOPORUČENO**

---

### Implementační strategie

**Incremental Rollout:**
1. Fáze 1-2: Vytvoření tab struktury (2 dny)
2. Testing checkpoint 1: ✅ Tabs fungují?
3. Fáze 3-4: Integrace + styling (2 dny)
4. Testing checkpoint 2: ✅ Workflow funguje?
5. Fáze 5-6: Polish + dokumentace (1 den)
6. Final release: Merge do `master`

**Rollback Plan:**
```bash
# Pokud cokoli selže
git checkout master
git branch -D feature/gui-tabs-redesign
```

---

### Otevřené otázky k diskusi

#### Q1: Window size

**Otázka:** Dynamický resize podle tabu, nebo fixed 700x550?

**Možnosti:**
- A) Dynamický: Translation 600x400, Settings 700x550
- B) Fixed: Vždy 700x550
- C) User resizable: min 600x400, max podle monitoru

**Doporučení:** **B (Fixed 700x550)** - konzistentnější, user si zvykne

---

#### Q2: Tlačítko "Zavřít"

**Otázka:** Kde umístit tlačítko Zavřít?

**Možnosti:**
- A) V každém tabu (duplikace)
- B) Globálně mimo tabs (header/footer)
- C) Pouze ESC / X button v titlebar

**Doporučení:** **C (Pouze ESC / titlebar X)** - tabs nepotřebují Zavřít

---

#### Q3: Live reload vs Uložit

**Otázka:** Ponechat [Uložit] tlačítko nebo auto-save?

**Možnosti:**
- A) [Uložit] tlačítko (současný stav)
- B) Auto-save on change
- C) [Uložit] + [Zrušit] (reset changes)

**Doporučení:** **A ([Uložit])** - bezpečnější, user kontroluje změny

---

#### Q4: Keyboard shortcuts

**Otázka:** Přidat Ctrl+1/2 pro tab switching?

**Možnosti:**
- A) Ctrl+1 = Translation, Ctrl+2 = Settings
- B) Ctrl+Tab = Next tab (standard)
- C) Obojí

**Doporučení:** **C (Obojí)** - max flexibility

---

#### Q5: Tab position

**Otázka:** Umístění tabs - nahoře nebo vlevo?

**Možnosti:**
- A) Nahoře (horizontal) - standard
- B) Vlevo (vertical) - sidebar style

**Doporučení:** **A (Nahoře)** - konzistentní s 99% aplikací

---

## 📚 7. REFERENCE A ZDROJE

### Dokumentace

- [Python Tkinter ttk.Notebook Tutorial](https://www.pythontutorial.net/tkinter/tkinter-notebook/)
- [Python Assets - Notebook Widget Guide](https://pythonassets.com/posts/notebook-widget-tabs-in-tk-tkinter/)
- [LikeGeeks - Tab Styling & Customization](https://likegeeks.com/tkinter-notebook-tab-styling-ttk/)

### UI/UX Best Practices

- [NN/Group - Tabs, Used Right](https://www.nngroup.com/articles/tabs-used-right/)
- [Eleken - Tabs UX: Best Practices](https://www.eleken.co/blog-posts/tabs-ux)
- [LogRocket - Tabbed Navigation in UX](https://blog.logrocket.com/ux-design/tabs-ux-best-practices/)
- [UX Design World - Tabs Navigation Design](https://uxdworld.com/tabs-navigation-design-best-practices/)

### Code Examples

- [GeeksforGeeks - ttk.Notebook Python](https://www.geeksforgeeks.org/python/access-the-actual-tab-widget-of-ttknotebook-in-python-tkinter/)
- [ProgramCreek - Tkinter Notebook Examples](https://www.programcreek.com/python/example/104109/tkinter.ttk.Notebook)

---

## 📝 8. CHANGELOG & UPDATES

| Datum | Autor | Změna |
|-------|-------|-------|
| 2025-01-29 | Claude Code | Vytvoření gui.md - Initial analysis & plan |
| TBD | Dev Team | Implementation start - Phase 1 |
| TBD | Dev Team | Testing & review |
| TBD | Dev Team | Merge do master |

---

## ✅ 9. NEXT STEPS

### Immediate Actions (tento týden)

- [ ] Review gui.md s týmem
- [ ] Diskuse otevřených otázek (Q1-Q5)
- [ ] Schválení implementačního plánu
- [ ] Git branch vytvoření
- [ ] Fáze 1 start (POC with 2 dummy tabs)

### Short-term (příští týden)

- [ ] Fáze 2-3: Refactoring + integrace
- [ ] Testing checkpoint 1
- [ ] Fáze 4-5: Styling + polish
- [ ] Testing checkpoint 2

### Long-term (příští měsíc)

- [ ] Merge do master
- [ ] Production deployment
- [ ] User feedback collection
- [ ] Možný třetí tab (Historie) - budoucí feature

---

**Konec dokumentu**

*Vytvořeno pomocí Claude Code s ULTRATHINK deep analysis*
*Datum: 2025-01-29*
*Verze: 1.0*
