# -*- coding: utf-8 -*-
"""
Modern Dark Theme s glow efekty a Fira Code fontem
"""

# Color Palette - Cyberpunk/Neon Dark Theme
COLORS = {
    # Pozadí
    "bg_dark": "#1e1e1e",           # Hlavní pozadí
    "bg_darker": "#151515",         # Tmavší pozadí
    "bg_input": "#252525",          # Input pole pozadí
    "bg_button": "#2a2a2a",         # Tlačítko pozadí
    "bg_button_hover": "#353535",   # Tlačítko hover

    # Text
    "text_primary": "#dadada",      # Hlavní text
    "text_secondary": "#999999",    # Sekundární text
    "text_muted": "#666666",        # Ztlumený text

    # Accent barvy s glow efektem
    "accent_cyan": "#00d9ff",       # Cyan - hlavní accent
    "accent_purple": "#b362ff",     # Purple
    "accent_green": "#50fa7b",      # Green - success
    "accent_red": "#ff5555",        # Red - error
    "accent_orange": "#ffb86c",     # Orange - warning
    "accent_pink": "#ff79c6",       # Pink

    # Borders
    "border": "#333333",
    "border_focus": "#00d9ff",      # Cyan glow při focusu

    # Status colors
    "status_ready": "#50fa7b",      # Zelená
    "status_working": "#00d9ff",    # Cyan
    "status_error": "#ff5555",      # Červená
    "status_warning": "#ffb86c",    # Oranžová
}

# Fonts
FONTS = {
    "mono": ("Fira Code", "Consolas", "Monaco", "Courier New", "monospace"),
    "sans": ("Segoe UI", "Arial", "sans-serif"),
    "size_normal": 10,
    "size_large": 12,
    "size_small": 8,
}

def get_ttk_theme_config():
    """Vrátí konfiguraci pro ttk theme"""
    return {
        "TFrame": {
            "background": COLORS["bg_dark"]
        },
        "TLabel": {
            "background": COLORS["bg_dark"],
            "foreground": COLORS["text_primary"],
            "font": FONTS["sans"] + (FONTS["size_normal"],)
        },
        "TButton": {
            "background": COLORS["bg_button"],
            "foreground": COLORS["accent_cyan"],
            "bordercolor": COLORS["border"],
            "focuscolor": COLORS["border_focus"],
            "lightcolor": COLORS["bg_button_hover"],
            "darkcolor": COLORS["bg_darker"],
            "font": FONTS["sans"] + (FONTS["size_normal"], "bold"),
            "padding": [10, 5]
        },
        "TEntry": {
            "fieldbackground": COLORS["bg_input"],
            "foreground": COLORS["text_primary"],
            "bordercolor": COLORS["border"],
            "lightcolor": COLORS["border_focus"],
            "insertcolor": COLORS["accent_cyan"],
            "font": FONTS["mono"] + (FONTS["size_normal"],)
        },
        "TCombobox": {
            "fieldbackground": COLORS["bg_input"],
            "background": COLORS["bg_button"],
            "foreground": COLORS["text_primary"],
            "arrowcolor": COLORS["accent_cyan"],
            "bordercolor": COLORS["border"],
            "font": FONTS["mono"] + (FONTS["size_normal"],)
        }
    }
