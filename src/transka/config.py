# -*- coding: utf-8 -*-
"""
Správa konfigurace aplikace DeepL Translator
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Logging setup
logger = logging.getLogger(__name__)

# Načtení .env souboru
load_dotenv()


class Config:
    """Správa konfigurace aplikace"""

    CONFIG_FILE = Path("config.json")
    ENV_FILE = Path(".env")

    DEFAULT_CONFIG = {
        "source_lang": "CS",
        "target_lang": "EN-US",
        "translator_service": "deepl",  # "deepl" nebo "google"
        "hotkey_main": "ctrl+alt+t",  # Hlavní zkratka: Ctrl+Alt+T (Translate)
        "hotkey_swap": "ctrl+alt+s",  # Swap jazyků: Ctrl+Alt+S
        "hotkey_clear": "ctrl+alt+c",  # Vymazání input pole: Ctrl+Alt+C
        "window_width": 600,
        "window_height": 400,
        "usage_warning_threshold": 480000  # Varování při 96% limitu (480k z 500k)
    }

    def __init__(self):
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.api_key: str = ""
        self.load()

    def load(self) -> None:
        """Načte konfiguraci ze souboru a .env"""
        # API klíč z .env
        import os
        self.api_key = os.getenv("DEEPL_API_KEY", "")

        # Ostatní nastavení z config.json
        if self.CONFIG_FILE.exists():
            try:
                config_data = self.CONFIG_FILE.read_text(encoding="utf-8")
                saved_config = json.loads(config_data)
                self.config.update(saved_config)
                logger.info(f"Konfigurace načtena z {self.CONFIG_FILE}")
            except Exception as e:
                logger.error(f"Chyba při načítání konfigurace: {e}", exc_info=True)

    def save(self) -> None:
        """Uloží konfiguraci do souboru"""
        try:
            config_data = json.dumps(self.config, indent=2, ensure_ascii=False)
            self.CONFIG_FILE.write_text(config_data, encoding="utf-8")
            logger.debug(f"Konfigurace uložena do {self.CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Chyba při ukládání konfigurace: {e}", exc_info=True)

    def get(self, key: str, default: Any = None) -> Any:
        """Získá hodnotu z konfigurace"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Nastaví hodnotu v konfiguraci"""
        self.config[key] = value
        self.save()

    def set_api_key(self, api_key: str) -> None:
        """Nastaví API klíč do .env souboru"""
        self.api_key = api_key

        # Uložení do .env souboru
        lines = []

        if self.ENV_FILE.exists():
            lines = self.ENV_FILE.read_text(encoding="utf-8").splitlines(keepends=True)

        # Aktualizace nebo přidání DEEPL_API_KEY
        key_found = False
        for i, line in enumerate(lines):
            if line.startswith("DEEPL_API_KEY="):
                lines[i] = f"DEEPL_API_KEY={api_key}\n"
                key_found = True
                break

        if not key_found:
            lines.append(f"DEEPL_API_KEY={api_key}\n")

        self.ENV_FILE.write_text("".join(lines), encoding="utf-8")
        logger.info("API klíč aktualizován v .env souboru")

    @property
    def source_lang(self) -> str:
        """Zdrojový jazyk"""
        return self.config["source_lang"]

    @property
    def target_lang(self) -> str:
        """Cílový jazyk"""
        return self.config["target_lang"]

    @property
    def hotkey_main(self) -> str:
        """Hlavní klávesová zkratka (Ctrl+Alt+T) - otevře okno / přeloží"""
        return self.config.get("hotkey_main", "ctrl+alt+t")  # Fallback pro staré konfigurace

    @property
    def hotkey_swap(self) -> str:
        """Zkratka pro swap jazyků (Ctrl+Alt+S)"""
        return self.config.get("hotkey_swap", "ctrl+alt+s")  # Fallback pro staré konfigurace

    @property
    def hotkey_clear(self) -> str:
        """Zkratka pro vymazání input pole (Ctrl+Alt+C)"""
        return self.config.get("hotkey_clear", "ctrl+alt+c")  # Fallback pro staré konfigurace

    @property
    def window_width(self) -> int:
        """Šířka okna"""
        return self.config["window_width"]

    @property
    def window_height(self) -> int:
        """Výška okna"""
        return self.config["window_height"]

    @property
    def usage_warning_threshold(self) -> int:
        """Práh varování pro spotřebu znaků"""
        return self.config["usage_warning_threshold"]

    @property
    def translator_service(self) -> str:
        """Vybraná překladová služba (deepl/google)"""
        return self.config.get("translator_service", "deepl")  # Fallback pro staré konfigurace
