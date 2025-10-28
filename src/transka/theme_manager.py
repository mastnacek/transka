# -*- coding: utf-8 -*-
"""
Theme Manager pro aplikaci Transka
Aplikuje modern dark theme s glow efekty na Tkinter okna
"""
import tkinter as tk
from tkinter import ttk, font as tkfont
from typing import Dict, Any

from transka.theme import COLORS, FONTS


class ThemeManager:
    """Správce aplikačního dark theme"""

    def __init__(self, root: tk.Tk):
        """
        Inicializuje ThemeManager

        Args:
            root: Hlavní Tkinter okno
        """
        self.root = root
        self.mono_font = None
        self.mono_font_large = None
        self.sans_font = None
        self.sans_font_bold = None

    def apply_theme(self):
        """Aplikuje kompletní dark theme na okno"""
        # Pozadí hlavního okna
        self.root.configure(bg=COLORS["bg_dark"])

        # Dark titlebar pro Windows
        self._apply_dark_titlebar()

        # Vytvoření fontů
        self._create_fonts()

        # TTK Style konfigurace
        self._configure_ttk_styles()

    def _apply_dark_titlebar(self):
        """Aplikuje dark titlebar pro Windows 11/10 (odstranění bílého pruhu nahoře)"""
        try:
            # Musíme počkat, než se okno vytvoří
            self.root.update_idletasks()

            import ctypes
            # Získání HWND handle přímo z winfo_id()
            hwnd = self.root.winfo_id()

            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20 (Windows 11)
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 19 (Windows 10 build 19041+)
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(2)  # 2 = force dark mode, 1 = enable

            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception as e:
            print(f"Dark titlebar nepodporován: {e}")  # Debug info

    def _create_fonts(self):
        """Vytvoří fonty pro aplikaci"""
        # Vytvoření Fira Code fontu
        try:
            self.mono_font = tkfont.Font(family="Fira Code", size=FONTS["size_normal"])
            self.mono_font_large = tkfont.Font(family="Fira Code", size=FONTS["size_large"])
        except:
            # Fallback na Consolas pokud Fira Code není k dispozici
            self.mono_font = tkfont.Font(family="Consolas", size=FONTS["size_normal"])
            self.mono_font_large = tkfont.Font(family="Consolas", size=FONTS["size_large"])

        self.sans_font = tkfont.Font(family="Segoe UI", size=FONTS["size_normal"])
        self.sans_font_bold = tkfont.Font(family="Segoe UI", size=FONTS["size_normal"], weight="bold")

    def _configure_ttk_styles(self):
        """Konfiguruje TTK styles pro dark theme"""
        style = ttk.Style()
        style.theme_use('clam')  # Používáme 'clam' theme jako základ

        # Frame style
        style.configure('TFrame', background=COLORS["bg_dark"])

        # Label style
        style.configure('TLabel',
            background=COLORS["bg_dark"],
            foreground=COLORS["text_primary"],
            font=self.sans_font
        )

        # Button style s glow efektem
        style.configure('TButton',
            background=COLORS["bg_button"],
            foreground=COLORS["accent_cyan"],
            bordercolor=COLORS["border"],
            focuscolor=COLORS["border_focus"],
            font=self.sans_font_bold,
            relief=tk.FLAT
        )
        style.map('TButton',
            background=[('active', COLORS["bg_button_hover"]), ('pressed', COLORS["bg_darker"])],
            foreground=[('active', COLORS["accent_cyan"]), ('pressed', COLORS["accent_purple"])]
        )

        # Entry style
        style.configure('TEntry',
            fieldbackground=COLORS["bg_input"],
            background=COLORS["bg_input"],
            foreground=COLORS["text_primary"],
            insertcolor=COLORS["accent_cyan"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border_focus"],
            darkcolor=COLORS["border"]
        )

        # Combobox style
        style.configure('TCombobox',
            fieldbackground=COLORS["bg_input"],
            background=COLORS["bg_button"],
            foreground=COLORS["text_primary"],
            arrowcolor=COLORS["accent_cyan"],
            bordercolor=COLORS["border"]
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', COLORS["bg_input"])],
            selectbackground=[('readonly', COLORS["accent_cyan"])],
            selectforeground=[('readonly', COLORS["bg_dark"])]
        )

    def get_fonts(self) -> Dict[str, Any]:
        """
        Vrátí slovník s vytvořenými fonty

        Returns:
            Dict s klíči: mono_font, mono_font_large, sans_font, sans_font_bold
        """
        return {
            "mono_font": self.mono_font,
            "mono_font_large": self.mono_font_large,
            "sans_font": self.sans_font,
            "sans_font_bold": self.sans_font_bold
        }
