# -*- coding: utf-8 -*-
"""
GUI Builder pro aplikaci Transka
Vytváří a konfiguruje GUI komponenty
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, Any, Callable

from transka.theme import COLORS


class GUIBuilder:
    """Builder pro vytvoření GUI komponent aplikace"""

    def __init__(
        self,
        root: tk.Tk,
        fonts: Dict[str, Any],
        translator_display: str,
        language_display: str,
        hotkey_main: str
    ):
        """
        Inicializuje GUIBuilder

        Args:
            root: Hlavní Tkinter okno
            fonts: Dict s fonty (mono_font, mono_font_large, sans_font, sans_font_bold)
            translator_display: Text pro zobrazení překladače
            language_display: Text pro zobrazení jazyků
            hotkey_main: Hlavní klávesová zkratka
        """
        self.root = root
        self.fonts = fonts
        self.translator_display = translator_display
        self.language_display = language_display
        self.hotkey_main = hotkey_main

        # Widgets (budou vytvořeny v build())
        self.input_text = None
        self.output_text = None
        self.status_label = None
        self.usage_label = None
        self.translator_label = None
        self.lang_label = None

    def build(
        self,
        on_translate: Callable[[], None],
        on_clear: Callable[[], None],
        on_settings: Callable[[], None],
        on_close: Callable[[], None]
    ) -> Dict[str, Any]:
        """
        Vytvoří všechny GUI komponenty

        Args:
            on_translate: Callback pro tlačítko Přeložit
            on_clear: Callback pro tlačítko Vymazat
            on_settings: Callback pro tlačítko Nastavení
            on_close: Callback pro tlačítko Zavřít

        Returns:
            Dict s vytvořenými widgety
        """
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfigurace grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Header s aktuálními jazyky a překladačem
        self._create_header(main_frame)

        # Input pole
        self._create_input_field(main_frame)

        # Output pole
        self._create_output_field(main_frame)

        # Status bar
        self._create_status_bar(main_frame)

        # Tlačítka
        self._create_buttons(main_frame, on_translate, on_clear, on_settings, on_close)

        return {
            "input_text": self.input_text,
            "output_text": self.output_text,
            "status_label": self.status_label,
            "usage_label": self.usage_label,
            "translator_label": self.translator_label,
            "lang_label": self.lang_label
        }

    def _create_header(self, parent: ttk.Frame):
        """Vytvoří header s překladačem a jazyky"""
        header_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Label pro překladač
        self.translator_label = tk.Label(
            header_frame,
            text=self.translator_display,
            fg=COLORS["accent_yellow"],
            bg=COLORS["bg_dark"],
            font=self.fonts["sans_font_bold"]
        )
        self.translator_label.pack(side=tk.LEFT, padx=(0, 15))

        # Label pro jazyky
        self.lang_label = tk.Label(
            header_frame,
            text=self.language_display,
            fg=COLORS["accent_cyan"],
            bg=COLORS["bg_dark"],
            font=self.fonts["sans_font_bold"]
        )
        self.lang_label.pack(side=tk.LEFT)

    def _create_input_field(self, parent: ttk.Frame):
        """Vytvoří input textové pole"""
        input_label = ttk.Label(parent, text="Text k překladu:")
        input_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

        self.input_text = scrolledtext.ScrolledText(
            parent,
            height=8,
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
        self.input_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Styling scrollbaru
        self.input_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            width=12
        )
        self.input_text.focus()

    def _create_output_field(self, parent: ttk.Frame):
        """Vytvoří output textové pole"""
        output_label = ttk.Label(parent, text="Přeložený text:")
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))

        self.output_text = scrolledtext.ScrolledText(
            parent,
            height=8,
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
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Styling scrollbaru
        self.output_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_purple"],
            relief=tk.FLAT,
            width=12
        )

    def _create_status_bar(self, parent: ttk.Frame):
        """Vytvoří status bar s počítadlem znaků"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        self.status_label = ttk.Label(
            status_frame,
            text="Připraveno",
            foreground=COLORS["text_primary"]
        )
        self.status_label.pack(side=tk.LEFT)

        self.usage_label = ttk.Label(
            status_frame,
            text="Načítám usage...",
            foreground=COLORS["text_secondary"]
        )
        self.usage_label.pack(side=tk.RIGHT)

    def _create_buttons(
        self,
        parent: ttk.Frame,
        on_translate: Callable[[], None],
        on_clear: Callable[[], None],
        on_settings: Callable[[], None],
        on_close: Callable[[], None]
    ):
        """Vytvoří tlačítka"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, pady=(10, 0))

        ttk.Button(
            button_frame,
            text=f"Přeložit ({self.hotkey_main})",
            command=on_translate
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Vymazat",
            command=on_clear
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Nastavení",
            command=on_settings
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Zavřít",
            command=on_close
        ).pack(side=tk.LEFT, padx=5)
