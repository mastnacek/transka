"""
DeepL API překladač - implementace BaseTranslator
"""
import deepl
from typing import Optional, Tuple, List

from transka.base_translator import BaseTranslator, UsageInfo


class DeepLTranslator(BaseTranslator):
    """DeepL API překladač s podporou usage monitoringu"""

    def __init__(self, api_key: str):
        """
        Inicializace DeepL překladače

        Args:
            api_key: DeepL API klíč
        """
        self.api_key = api_key
        self.translator: Optional[deepl.Translator] = None
        self._initialize_translator()

    def _initialize_translator(self) -> None:
        """Inicializace DeepL translatoru"""
        if not self.api_key:
            return

        try:
            self.translator = deepl.Translator(self.api_key)
        except Exception as e:
            print(f"Chyba při inicializaci DeepL API: {e}")
            self.translator = None

    def is_configured(self) -> bool:
        """Kontrola, zda je translator nakonfigurován"""
        return self.translator is not None

    def translate(
        self,
        text: str,
        source_lang: str = "CS",
        target_lang: str = "EN-US"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Přeloží text pomocí DeepL API

        Args:
            text: Text k překladu
            source_lang: Zdrojový jazyk (např. "CS", "EN")
            target_lang: Cílový jazyk (např. "EN-US", "CS")

        Returns:
            Tuple (přeložený text, chybová zpráva)
        """
        if not self.translator:
            return None, "DeepL API není nakonfigurováno. Nastavte API klíč."

        if not text or not text.strip():
            return None, "Prázdný text k překladu"

        try:
            # Překlad textu
            result = self.translator.translate_text(
                text,
                source_lang=source_lang if source_lang != "AUTO" else None,
                target_lang=target_lang
            )

            return result.text, None

        except deepl.AuthorizationException:
            return None, "Neplatný API klíč. Zkontrolujte nastavení."
        except deepl.QuotaExceededException:
            return None, "Překročen limit znaků. Navštivte DeepL pro upgrade."
        except deepl.DeepLException as e:
            return None, f"DeepL API chyba: {str(e)}"
        except Exception as e:
            return None, f"Neočekávaná chyba: {str(e)}"

    def get_usage(self) -> Tuple[Optional[UsageInfo], Optional[str]]:
        """
        Získá informace o spotřebě API

        Returns:
            Tuple (UsageInfo, chybová zpráva)
        """
        if not self.translator:
            return None, "DeepL API není nakonfigurováno"

        try:
            usage = self.translator.get_usage()

            # Free API používá character, Pro API může používat i document
            if usage.character:
                info = UsageInfo(
                    character_count=usage.character.count,
                    character_limit=usage.character.limit,
                    service_name="DeepL"
                )
                return info, None
            else:
                return None, "Nelze získat informace o spotřebě"

        except deepl.AuthorizationException:
            return None, "Neplatný API klíč"
        except deepl.DeepLException as e:
            return None, f"DeepL API chyba: {str(e)}"
        except Exception as e:
            return None, f"Chyba při získávání usage: {str(e)}"

    def get_available_languages(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """
        Získá seznam dostupných jazyků

        Returns:
            Tuple (zdrojové jazyky, cílové jazyky)
        """
        if not self.translator:
            return [], []

        try:
            source_langs = self.translator.get_source_languages()
            target_langs = self.translator.get_target_languages()

            source_list = [(lang.code, lang.name) for lang in source_langs]
            target_list = [(lang.code, lang.name) for lang in target_langs]

            return source_list, target_list

        except Exception as e:
            print(f"Chyba při získávání jazyků: {e}")
            return [], []

    def update_api_key(self, api_key: str) -> None:
        """Aktualizuje API klíč"""
        self.api_key = api_key
        self._initialize_translator()

    @property
    def service_name(self) -> str:
        """Název služby"""
        return "DeepL"
