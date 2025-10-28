# -*- coding: utf-8 -*-
"""
Google Translate API překladač - implementace BaseTranslator
Používá googletrans knihovnu (free, bez API klíče)
"""
from typing import Optional, Tuple, List
from googletrans import Translator as GoogleTranslatorLib, LANGUAGES

from transka.base_translator import BaseTranslator, UsageInfo


class GoogleTranslator(BaseTranslator):
    """
    Google Translate překladač pomocí googletrans knihovny

    Free verze - nepotřebuje API klíč, ale není zaručena stabilita.
    Vhodné jako fallback, když DeepL dosáhne limitu.
    """

    def __init__(self, api_key: str = ""):
        """
        Inicializace Google Translate překladače

        Args:
            api_key: Nepoužito (googletrans je free bez API klíče)
        """
        self.translator = GoogleTranslatorLib()
        self._usage_count = 0  # Lokální počítadlo znaků
        self.api_key = api_key  # Uloženo pro kompatibilitu s BaseTranslator

    def is_configured(self) -> bool:
        """Kontrola, zda je translator nakonfigurován"""
        # Google Translate free API nepotřebuje klíč
        return True

    def translate(
        self,
        text: str,
        source_lang: str = "CS",
        target_lang: str = "EN-US"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Přeloží text pomocí Google Translate API

        Args:
            text: Text k překladu (max 15,000 znaků)
            source_lang: Jazyk zdroje (AUTO pro auto-detekci, CS, EN, atd.)
            target_lang: Cílový jazyk (EN-US, CS, atd.)

        Returns:
            Tuple[přeložený_text, chyba]
        """
        if not text or not text.strip():
            return None, "Prázdný text"

        try:
            # Konverze formátu jazyků z DeepL na googletrans
            # DeepL: "CS", "EN-US", "AUTO" -> googletrans: "cs", "en", "auto"
            src = self._convert_lang_code(source_lang, is_source=True)
            dest = self._convert_lang_code(target_lang, is_source=False)

            # Překlad
            result = self.translator.translate(text, src=src, dest=dest)

            # Aktualizace počítadla
            self._usage_count += len(text)

            return result.text, None

        except Exception as e:
            error_msg = f"Google Translate chyba: {str(e)}"
            return None, error_msg

    def _convert_lang_code(self, lang_code: str, is_source: bool = False) -> str:
        """
        Konvertuje kód jazyka z DeepL formátu na googletrans formát

        Args:
            lang_code: Kód jazyka (např. "EN-US", "CS", "AUTO")
            is_source: True pokud je to zdrojový jazyk (podporuje AUTO)

        Returns:
            Konvertovaný kód (např. "en", "cs", "auto")
        """
        # Speciální případy
        if is_source and lang_code.upper() == "AUTO":
            return "auto"

        # Rozdělit na jazyk a region (EN-US -> en)
        base_lang = lang_code.split('-')[0].lower()

        # Speciální mapování pro čínštinu
        if base_lang == "zh":
            if "CN" in lang_code.upper() or "HANS" in lang_code.upper():
                return "zh-cn"
            elif "TW" in lang_code.upper() or "HANT" in lang_code.upper():
                return "zh-tw"

        return base_lang

    def get_usage(self) -> Tuple[Optional[UsageInfo], Optional[str]]:
        """
        Získá informace o spotřebě API

        Google Translate free API nemá oficiální limity ani usage tracking.
        Vrací lokální počítadlo s "neomezeným" limitem.

        Returns:
            Tuple[UsageInfo, chyba]
        """
        info = UsageInfo(
            character_count=self._usage_count,
            character_limit=999999999,  # "Neomezeno" (free verze)
            service_name="Google Translate (Free)"
        )
        return info, None

    def get_available_languages(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """
        Získá seznam dostupných jazyků z googletrans.LANGUAGES

        Returns:
            Tuple[source_langs, target_langs] - Google podporuje stejné jazyky pro oba směry
        """
        # Vytvoření seznamu z LANGUAGES dictionary
        langs = []

        # Přidání AUTO pro zdrojový jazyk
        source_langs = [("AUTO", "Automatická detekce")]

        # Běžné jazyky na začátek
        priority_langs = [
            ("cs", "Čeština"),
            ("en", "Angličtina"),
            ("de", "Němčina"),
            ("fr", "Francouzština"),
            ("es", "Španělština"),
            ("it", "Italština"),
            ("pl", "Polština"),
            ("ru", "Ruština"),
        ]

        # Přidat prioritní jazyky
        langs.extend(priority_langs)

        # Přidat ostatní jazyky z LANGUAGES (bez duplikátů)
        priority_codes = {code for code, _ in priority_langs}
        for code, name in sorted(LANGUAGES.items(), key=lambda x: x[1]):
            if code not in priority_codes and code != "auto":
                # Kapitalizace prvního písmene názvu
                langs.append((code, name.capitalize()))

        # Source languages obsahují AUTO + všechny jazyky
        source_langs.extend(langs)

        # Target languages neobsahují AUTO
        target_langs = langs.copy()

        return source_langs, target_langs

    def update_api_key(self, api_key: str) -> None:
        """Aktualizuje API klíč (u Google Translate není potřeba)"""
        self.api_key = api_key

    @property
    def service_name(self) -> str:
        """Název služby"""
        return "Google Translate"
