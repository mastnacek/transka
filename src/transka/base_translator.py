# -*- coding: utf-8 -*-
"""
Abstraktní rozhraní pro překladače
Umožňuje snadné přepínání mezi DeepL a Google Translate
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class UsageInfo:
    """Informace o spotřebě API"""
    character_count: int
    character_limit: int
    service_name: str = "Unknown"

    @property
    def usage_percentage(self) -> float:
        """Procento využití limitu"""
        if self.character_limit == 0:
            return 0.0
        return (self.character_count / self.character_limit) * 100

    @property
    def formatted_usage(self) -> str:
        """Formátované zobrazení spotřeby"""
        return f"{self.character_count:,} / {self.character_limit:,} znaků ({self.usage_percentage:.1f}%)"

    @property
    def is_near_limit(self) -> bool:
        """Kontrola, zda se blížíme limitu (>95%)"""
        return self.usage_percentage > 95.0


class BaseTranslator(ABC):
    """Abstraktní třída pro všechny překladače"""

    @abstractmethod
    def is_configured(self) -> bool:
        """Kontrola, zda je translator nakonfigurován"""
        pass

    @abstractmethod
    def translate(
        self,
        text: str,
        source_lang: str = "CS",
        target_lang: str = "EN-US"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Přeloží text

        Args:
            text: Text k překladu
            source_lang: Zdrojový jazyk
            target_lang: Cílový jazyk

        Returns:
            Tuple (přeložený text, chybová zpráva)
        """
        pass

    @abstractmethod
    def get_usage(self) -> Tuple[Optional[UsageInfo], Optional[str]]:
        """
        Získá informace o spotřebě API

        Returns:
            Tuple (UsageInfo, chybová zpráva)
        """
        pass

    @abstractmethod
    def get_available_languages(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """
        Získá seznam dostupných jazyků

        Returns:
            Tuple (zdrojové jazyky, cílové jazyky)
        """
        pass

    @abstractmethod
    def update_api_key(self, api_key: str) -> None:
        """Aktualizuje API klíč"""
        pass

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Název služby (DeepL, Google, atd.)"""
        pass
