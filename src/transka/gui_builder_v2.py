# -*- coding: utf-8 -*-
"""
GUI Builder V2 pro aplikaci Transka - Tab-based interface
Kombinuje překlad a nastavení do jednoho okna s tabs
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, Any, Callable

from transka.theme import COLORS
from transka.config import Config
from transka.deepl_translator import DeepLTranslator
from transka.base_translator import BaseTranslator


class GUIBuilderV2:
    """Builder pro vytvoření GUI s tab-based interface"""

    def __init__(
        self,
        root: tk.Tk,
        fonts: Dict[str, Any],
        translator_display: str,
        language_display: str,
        hotkey_main: str,
        config: Config,
        translator: BaseTranslator,
        parent_app=None
    ):
        """
        Inicializuje GUIBuilderV2

        Args:
            root: Hlavní Tkinter okno
            fonts: Dict s fonty (mono_font, mono_font_large, sans_font, sans_font_bold)
            translator_display: Text pro zobrazení překladače
            language_display: Text pro zobrazení jazyků
            hotkey_main: Hlavní klávesová zkratka
            config: Config instance pro nastavení
            translator: BaseTranslator instance
            parent_app: Reference na TranslatorApp pro live reload
        """
        self.root = root
        self.fonts = fonts
        self.translator_display = translator_display
        self.language_display = language_display
        self.hotkey_main = hotkey_main
        self.config = config
        self.translator = translator
        self.parent_app = parent_app

        # Tab frames
        self.translation_tab = None
        self.settings_tab = None
        self.current_tab = None

        # Tab buttons (Frame)
        self.translation_tab_btn = None
        self.settings_tab_btn = None
        # Tab labels (Label inside Frame)
        self.translation_tab_label = None
        self.settings_tab_label = None
        self.content_container = None

        # Translation widgets
        self.input_text = None
        self.output_text = None
        self.status_label = None
        self.usage_label = None
        self.translator_label = None
        self.lang_label = None

        # Settings widgets
        self.translator_service_var = None
        self.translator_service_combo = None
        self.api_key_entry = None
        self.source_lang_var = None
        self.source_lang_combo = None
        self.target_lang_var = None
        self.target_lang_combo = None
        self.hotkey_main_entry = None
        self.hotkey_swap_entry = None
        self.hotkey_clear_entry = None
        self.warning_threshold_entry = None

        # Placeholder state
        self.placeholder_active = False

    def build(
        self,
        on_translate: Callable[[], None],
        on_clear: Callable[[], None],
        on_save_settings: Callable[[], None],
        on_test_api: Callable[[], None],
        on_close: Callable[[], None]
    ) -> Dict[str, Any]:
        """
        Vytvoří všechny GUI komponenty s tabs

        Args:
            on_translate: Callback pro tlačítko Přeložit
            on_clear: Callback pro tlačítko Vymazat
            on_save_settings: Callback pro uložení nastavení
            on_test_api: Callback pro test API
            on_close: Callback pro zavření okna

        Returns:
            Dict s vytvořenými widgety
        """
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Grid configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Header (global - mimo tabs)
        self._create_header(main_frame)

        # Custom tab buttons (místo ttk.Notebook)
        self._create_tab_buttons(main_frame)

        # Container pro tab content - SUNKEN border pro vizuální hloubku
        self.content_container = tk.Frame(
            main_frame,
            relief=tk.SUNKEN,
            borderwidth=2,
            bg=COLORS["bg_dark"]
        )
        self.content_container.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=(0, 0))
        self.content_container.columnconfigure(0, weight=1)
        self.content_container.rowconfigure(0, weight=1)

        # Create tabs
        self.translation_tab = self._create_translation_tab(on_translate, on_clear, on_close)
        self.settings_tab = self._create_settings_tab(on_save_settings, on_test_api)

        # Place tabs in container
        self.translation_tab.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.settings_tab.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Show translation tab by default
        self.current_tab = "translation"
        self.translation_tab.tkraise()

        # Přidat placeholder text do input pole
        self._add_placeholder_to_input()

        return {
            "input_text": self.input_text,
            "output_text": self.output_text,
            "status_label": self.status_label,
            "usage_label": self.usage_label,
            "translator_label": self.translator_label,
            "lang_label": self.lang_label
        }

    def _add_placeholder_to_input(self):
        """Přidá placeholder text do input pole"""
        placeholder_text = "💡 Tip: Vložte nebo napište text, který chcete přeložit...\n\nZkratky:\n• Ctrl+Enter - Přeložit\n• Ctrl+1 - Překlad tab\n• Ctrl+2 - Nastavení tab"

        # Vložit placeholder
        self.input_text.insert("1.0", placeholder_text)
        self.input_text.config(fg=COLORS["text_muted"])

        # Flag pro sledování placeholder stavu
        self.placeholder_active = True

        # Bind události
        self.input_text.bind("<FocusIn>", self._on_input_focus_in)
        self.input_text.bind("<FocusOut>", self._on_input_focus_out)

    def _on_input_focus_in(self, event):
        """Smaže placeholder při získání focusu"""
        if self.placeholder_active:
            self.input_text.delete("1.0", "end")
            self.input_text.config(fg=COLORS["text_primary"])
            self.placeholder_active = False

    def _on_input_focus_out(self, event):
        """Přidá placeholder zpět pokud je pole prázdné"""
        if not self.input_text.get("1.0", "end-1c").strip():
            placeholder_text = "💡 Tip: Vložte nebo napište text, který chcete přeložit...\n\nZkratky:\n• Ctrl+Enter - Přeložit\n• Ctrl+1 - Překlad tab\n• Ctrl+2 - Nastavení tab"
            self.input_text.insert("1.0", placeholder_text)
            self.input_text.config(fg=COLORS["text_muted"])
            self.placeholder_active = True

    def _create_header(self, parent: ttk.Frame):
        """Vytvoří header s překladačem a jazyky (globální mimo tabs)"""
        header_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(5, 15))

        # Label pro překladač - větší font
        from tkinter import font as tkfont
        header_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        self.translator_label = tk.Label(
            header_frame,
            text=self.translator_display,
            fg=COLORS["accent_yellow"],
            bg=COLORS["bg_dark"],
            font=header_font
        )
        self.translator_label.pack(side=tk.LEFT, padx=(0, 20))

        # Label pro jazyky - větší font
        self.lang_label = tk.Label(
            header_frame,
            text=self.language_display,
            fg=COLORS["accent_cyan"],
            bg=COLORS["bg_dark"],
            font=header_font
        )
        self.lang_label.pack(side=tk.LEFT)

    def _create_tab_buttons(self, parent: ttk.Frame):
        """Vytvoří vlastní tab tlačítka s border styling a hover efekty"""
        # Tab bar container
        tab_bar_container = tk.Frame(parent, bg=COLORS["bg_dark"])
        tab_bar_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 0))

        tab_frame = tk.Frame(tab_bar_container, bg=COLORS["bg_dark"], height=45)
        tab_frame.pack(fill=tk.X, padx=0, pady=0)
        tab_frame.pack_propagate(False)

        # Tab button pro Překlad - SUNKEN (aktivní)
        self.translation_tab_btn = tk.Frame(
            tab_frame,
            relief=tk.SUNKEN,
            borderwidth=2,
            bg=COLORS["bg_dark"],
            cursor="hand2"
        )
        self.translation_tab_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.translation_tab_label = tk.Label(
            self.translation_tab_btn,
            text="📝  Překlad",
            bg=COLORS["bg_dark"],
            fg=COLORS["accent_cyan"],
            font=self.fonts["sans_font_bold"],
            cursor="hand2"
        )
        self.translation_tab_label.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        # Bind click a hover events pro translation tab
        self.translation_tab_btn.bind("<Button-1>", lambda e: self.switch_to_translation_tab())
        self.translation_tab_label.bind("<Button-1>", lambda e: self.switch_to_translation_tab())
        self.translation_tab_btn.bind("<Enter>", lambda e: self._on_tab_hover_enter("translation"))
        self.translation_tab_btn.bind("<Leave>", lambda e: self._on_tab_hover_leave("translation"))
        self.translation_tab_label.bind("<Enter>", lambda e: self._on_tab_hover_enter("translation"))
        self.translation_tab_label.bind("<Leave>", lambda e: self._on_tab_hover_leave("translation"))

        # Tab button pro Nastavení - RAISED (neaktivní)
        self.settings_tab_btn = tk.Frame(
            tab_frame,
            relief=tk.RAISED,
            borderwidth=2,
            bg=COLORS["bg_darker"],
            cursor="hand2"
        )
        self.settings_tab_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.settings_tab_label = tk.Label(
            self.settings_tab_btn,
            text="⚙️  Nastavení",
            bg=COLORS["bg_darker"],
            fg=COLORS["text_secondary"],
            font=self.fonts["sans_font"],
            cursor="hand2"
        )
        self.settings_tab_label.pack(fill=tk.BOTH, expand=True, padx=18, pady=10)

        # Bind click a hover events pro settings tab
        self.settings_tab_btn.bind("<Button-1>", lambda e: self.switch_to_settings_tab())
        self.settings_tab_label.bind("<Button-1>", lambda e: self.switch_to_settings_tab())
        self.settings_tab_btn.bind("<Enter>", lambda e: self._on_tab_hover_enter("settings"))
        self.settings_tab_btn.bind("<Leave>", lambda e: self._on_tab_hover_leave("settings"))
        self.settings_tab_label.bind("<Enter>", lambda e: self._on_tab_hover_enter("settings"))
        self.settings_tab_label.bind("<Leave>", lambda e: self._on_tab_hover_leave("settings"))

        # Separator line - neon cyan accent
        separator = tk.Frame(
            tab_bar_container,
            bg=COLORS["accent_cyan"],
            height=2
        )
        separator.pack(fill=tk.X, padx=0, pady=0)

    def _create_translation_tab(
        self,
        on_translate: Callable[[], None],
        on_clear: Callable[[], None],
        on_close: Callable[[], None]
    ) -> ttk.Frame:
        """Vytvoří tab pro překlad"""
        frame = ttk.Frame(self.content_container)

        # Konfigurace grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

        # Input pole
        input_label = ttk.Label(
            frame,
            text="📝 Text k překladu:",
            font=self.fonts["sans_font_bold"]
        )
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(8, 6))

        self.input_text = scrolledtext.ScrolledText(
            frame,
            height=10,
            wrap=tk.WORD,
            font=self.fonts["mono_font_large"],
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            selectbackground=COLORS["accent_cyan"],
            selectforeground=COLORS["bg_dark"],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=COLORS["border_focus"],
            highlightbackground=COLORS["border"]
        )
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 12))

        # Styling scrollbaru
        self.input_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            width=12
        )

        # Output pole
        output_label = ttk.Label(
            frame,
            text="✨ Přeložený text:",
            font=self.fonts["sans_font_bold"]
        )
        output_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 6))

        self.output_text = scrolledtext.ScrolledText(
            frame,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=self.fonts["mono_font_large"],
            bg=COLORS["bg_darker"],
            fg=COLORS["text_primary"],
            selectbackground=COLORS["accent_purple"],
            selectforeground=COLORS["bg_dark"],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=COLORS["accent_purple"],
            highlightbackground=COLORS["border"]
        )
        self.output_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 12))

        # Styling scrollbaru
        self.output_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_purple"],
            relief=tk.FLAT,
            width=12
        )

        # Status bar s lepším stylingem
        status_frame = ttk.Frame(frame)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(8, 5))

        self.status_label = ttk.Label(
            status_frame,
            text="✅ Připraveno",
            foreground=COLORS["status_ready"],
            font=self.fonts["sans_font"]
        )
        self.status_label.pack(side=tk.LEFT)

        self.usage_label = ttk.Label(
            status_frame,
            text="📊 Načítám usage...",
            foreground=COLORS["text_secondary"],
            font=self.fonts["sans_font"]
        )
        self.usage_label.pack(side=tk.RIGHT)

        # Tlačítka s ikonami a lepším stylingem
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, pady=(15, 10))

        # Primární tlačítko - Přeložit
        translate_btn = ttk.Button(
            button_frame,
            text="🌐 Přeložit (Ctrl+Enter)",
            command=on_translate
        )
        translate_btn.pack(side=tk.LEFT, padx=6, ipady=4)

        # Sekundární tlačítko - Vymazat
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Vymazat",
            command=on_clear
        )
        clear_btn.pack(side=tk.LEFT, padx=6, ipady=4)

        # Sekundární tlačítko - Zavřít
        close_btn = ttk.Button(
            button_frame,
            text="✖️ Zavřít",
            command=on_close
        )
        close_btn.pack(side=tk.LEFT, padx=6, ipady=4)

        return frame

    def _create_settings_tab(
        self,
        on_save: Callable[[], None],
        on_test_api: Callable[[], None]
    ) -> ttk.Frame:
        """Vytvoří tab pro nastavení"""
        # Main frame pro settings
        main_settings_frame = ttk.Frame(self.content_container, padding="10")

        # Scrollable frame (pokud settings přeteče)
        canvas = tk.Canvas(main_settings_frame, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_settings_frame, orient="vertical", command=canvas.yview)
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
        main_settings_frame.columnconfigure(0, weight=1)
        main_settings_frame.rowconfigure(0, weight=1)

        # Settings widgets
        row = 0

        # Překladová služba
        ttk.Label(scrollable_frame, text="Překladač:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.translator_service_var = tk.StringVar()
        self.translator_service_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.translator_service_var,
            values=["deepl", "google"],
            state="readonly",
            width=47
        )
        self.translator_service_combo.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # API klíč
        ttk.Label(scrollable_frame, text="DeepL API klíč:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(scrollable_frame, width=50, show="*")
        self.api_key_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Zdrojový jazyk
        ttk.Label(scrollable_frame, text="Zdrojový jazyk:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.source_lang_var = tk.StringVar()
        self.source_lang_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.source_lang_var,
            values=["AUTO", "CS", "EN", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.source_lang_combo.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Cílový jazyk
        ttk.Label(scrollable_frame, text="Cílový jazyk:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.target_lang_var = tk.StringVar()
        self.target_lang_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.target_lang_var,
            values=["CS", "EN-US", "EN-GB", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.target_lang_combo.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Separator pro klávesové zkratky
        ttk.Separator(scrollable_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1

        ttk.Label(
            scrollable_frame,
            text="── Klávesové zkratky ──",
            font=self.fonts["sans_font_bold"]
        ).grid(row=row, column=0, columnspan=2, pady=(0, 10))
        row += 1

        # Klávesová zkratka - hlavní
        ttk.Label(scrollable_frame, text="Hlavní zkratka:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.hotkey_main_entry = ttk.Entry(scrollable_frame, width=50)
        self.hotkey_main_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(
            scrollable_frame,
            text="Formát: ctrl+p (dvojité stisknutí = Ctrl+P+P)",
            font=("", 8),
            foreground="gray"
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=0, padx=5)
        row += 1

        # Klávesová zkratka - swap jazyků
        ttk.Label(scrollable_frame, text="Swap jazyků:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.hotkey_swap_entry = ttk.Entry(scrollable_frame, width=50)
        self.hotkey_swap_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(
            scrollable_frame,
            text="Formát: ctrl+s (dvojité stisknutí = Ctrl+S+S)",
            font=("", 8),
            foreground="gray"
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=0, padx=5)
        row += 1

        # Klávesová zkratka - vymazání input pole
        ttk.Label(scrollable_frame, text="Vymazat input:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.hotkey_clear_entry = ttk.Entry(scrollable_frame, width=50)
        self.hotkey_clear_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(
            scrollable_frame,
            text="Formát: ctrl+c (dvojité stisknutí = Ctrl+C+C)",
            font=("", 8),
            foreground="gray"
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=0, padx=5)
        row += 1

        # Práh varování
        ttk.Label(scrollable_frame, text="Varování při (znacích):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.warning_threshold_entry = ttk.Entry(scrollable_frame, width=50)
        self.warning_threshold_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Tlačítka s ikonami
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        save_btn = ttk.Button(
            button_frame,
            text="💾 Uložit nastavení",
            command=on_save
        )
        save_btn.pack(side=tk.LEFT, padx=6, ipady=4)

        test_btn = ttk.Button(
            button_frame,
            text="🧪 Test API",
            command=on_test_api
        )
        test_btn.pack(side=tk.LEFT, padx=6, ipady=4)

        # Načíst aktuální hodnoty
        self._load_settings_values()

        return main_settings_frame

    def _load_settings_values(self):
        """Načte aktuální hodnoty do settings formuláře"""
        self.translator_service_var.set(self.config.translator_service)
        self.api_key_entry.insert(0, self.config.api_key)
        self.source_lang_var.set(self.config.source_lang)
        self.target_lang_var.set(self.config.target_lang)
        self.hotkey_main_entry.insert(0, self.config.hotkey_main)
        self.hotkey_swap_entry.insert(0, self.config.hotkey_swap)
        self.hotkey_clear_entry.insert(0, self.config.hotkey_clear)
        self.warning_threshold_entry.insert(0, str(self.config.usage_warning_threshold))

    def _update_tab_styles(self):
        """Aktualizuje styling tab buttonů podle aktivního tabu"""
        if self.current_tab == "translation":
            # Translation tab je aktivní - SUNKEN
            self.translation_tab_btn.config(
                relief=tk.SUNKEN,
                bg=COLORS["bg_dark"]
            )
            self.translation_tab_label.config(
                bg=COLORS["bg_dark"],
                fg=COLORS["accent_cyan"],
                font=self.fonts["sans_font_bold"]
            )
            # Settings tab je neaktivní - RAISED
            self.settings_tab_btn.config(
                relief=tk.RAISED,
                bg=COLORS["bg_darker"]
            )
            self.settings_tab_label.config(
                bg=COLORS["bg_darker"],
                fg=COLORS["text_secondary"],
                font=self.fonts["sans_font"]
            )
        else:
            # Settings tab je aktivní - SUNKEN
            self.settings_tab_btn.config(
                relief=tk.SUNKEN,
                bg=COLORS["bg_dark"]
            )
            self.settings_tab_label.config(
                bg=COLORS["bg_dark"],
                fg=COLORS["accent_cyan"],
                font=self.fonts["sans_font_bold"]
            )
            # Translation tab je neaktivní - RAISED
            self.translation_tab_btn.config(
                relief=tk.RAISED,
                bg=COLORS["bg_darker"]
            )
            self.translation_tab_label.config(
                bg=COLORS["bg_darker"],
                fg=COLORS["text_secondary"],
                font=self.fonts["sans_font"]
            )

    def get_settings_values(self) -> Dict[str, Any]:
        """Vrátí aktuální hodnoty z settings formuláře"""
        return {
            "translator_service": self.translator_service_var.get(),
            "api_key": self.api_key_entry.get().strip(),
            "source_lang": self.source_lang_var.get(),
            "target_lang": self.target_lang_var.get(),
            "hotkey_main": self.hotkey_main_entry.get().strip(),
            "hotkey_swap": self.hotkey_swap_entry.get().strip(),
            "hotkey_clear": self.hotkey_clear_entry.get().strip(),
            "usage_warning_threshold": self.warning_threshold_entry.get().strip()
        }

    def _on_tab_hover_enter(self, tab_name: str):
        """Hover efekt při najetí myší na tab"""
        # Pokud tab NENÍ aktivní, zobraz hover efekt
        if tab_name == "translation" and self.current_tab != "translation":
            self.translation_tab_btn.config(bg=COLORS["bg_input"])
            self.translation_tab_label.config(
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"]
            )
        elif tab_name == "settings" and self.current_tab != "settings":
            self.settings_tab_btn.config(bg=COLORS["bg_input"])
            self.settings_tab_label.config(
                bg=COLORS["bg_input"],
                fg=COLORS["text_primary"]
            )

    def _on_tab_hover_leave(self, tab_name: str):
        """Hover efekt při opuštění myší z tabu"""
        # Pokud tab NENÍ aktivní, vrať původní styl
        if tab_name == "translation" and self.current_tab != "translation":
            self.translation_tab_btn.config(bg=COLORS["bg_darker"])
            self.translation_tab_label.config(
                bg=COLORS["bg_darker"],
                fg=COLORS["text_secondary"]
            )
        elif tab_name == "settings" and self.current_tab != "settings":
            self.settings_tab_btn.config(bg=COLORS["bg_darker"])
            self.settings_tab_label.config(
                bg=COLORS["bg_darker"],
                fg=COLORS["text_secondary"]
            )

    def switch_to_translation_tab(self):
        """Přepne na Translation tab (Ctrl+1)"""
        self.current_tab = "translation"
        self.translation_tab.tkraise()
        self._update_tab_styles()
        self.input_text.focus()

    def switch_to_settings_tab(self):
        """Přepne na Settings tab (Ctrl+2)"""
        self.current_tab = "settings"
        self.settings_tab.tkraise()
        self._update_tab_styles()

    def get_input_text(self) -> str:
        """
        Vrátí text z input pole (ignoruje placeholder)

        Returns:
            String s textem, nebo prázdný string pokud je aktivní placeholder
        """
        if self.placeholder_active:
            return ""
        return self.input_text.get("1.0", "end-1c").strip()

    def clear_placeholder_if_active(self):
        """Vymaže placeholder pokud je aktivní (např. při paste)"""
        if self.placeholder_active:
            self.input_text.delete("1.0", "end")
            self.input_text.config(fg=COLORS["text_primary"])
            self.placeholder_active = False
