# -*- coding: utf-8 -*-
"""
Translation Workflow Manager pro aplikaci Transka
Spravuje 3-step překlad workflow s state machine
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import pyperclip
from typing import Optional, Callable
import ctypes

from transka.base_translator import BaseTranslator
from transka.theme import COLORS


class TranslationWorkflow:
    """Správce workflow pro překlad textu (3-step process)"""

    # State machine stavy
    STATE_HIDDEN = 0
    STATE_SHOWN = 1
    STATE_TRANSLATED = 2

    def __init__(
        self,
        translator: BaseTranslator,
        source_lang: str,
        target_lang: str,
        input_widget: scrolledtext.ScrolledText,
        output_widget: scrolledtext.ScrolledText,
        status_callback: Callable[[str, str], None],
        usage_update_callback: Callable[[], None]
    ):
        """
        Inicializuje TranslationWorkflow

        Args:
            translator: Instance překladače (DeepL/Google)
            source_lang: Zdrojový jazyk
            target_lang: Cílový jazyk
            input_widget: Input ScrolledText widget
            output_widget: Output ScrolledText widget
            status_callback: Callback pro update status labelu (text, color)
            usage_update_callback: Callback pro update usage statistik
        """
        self.translator = translator
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.input_widget = input_widget
        self.output_widget = output_widget
        self.status_callback = status_callback
        self.usage_update_callback = usage_update_callback

        # State pro workflow
        self.state = self.STATE_HIDDEN
        self.previous_window = None

    def update_translator(self, translator: BaseTranslator):
        """Aktualizuje překladač (při změně v Settings)"""
        self.translator = translator

    def update_languages(self, source_lang: str, target_lang: str):
        """Aktualizuje jazyky (při změně v Settings)"""
        self.source_lang = source_lang
        self.target_lang = target_lang

    def save_previous_window(self):
        """Uloží předchozí aktivní okno pro pozdější restore fokus"""
        try:
            self.previous_window = ctypes.windll.user32.GetForegroundWindow()
        except:
            self.previous_window = None

    def restore_previous_window(self):
        """Obnoví fokus na předchozí okno"""
        if self.previous_window:
            try:
                ctypes.windll.user32.SetForegroundWindow(self.previous_window)
            except:
                pass

    def translate_with_display(self, root: tk.Tk):
        """
        Přeloží text a zobrazí v output poli (NEUZAVŘE okno, NEKOPÍRUJE)
        Použito ve State 1 → State 2
        """
        input_text = self.input_widget.get("1.0", tk.END).strip()

        if not input_text:
            return

        if not self.translator.is_configured():
            messagebox.showerror("Chyba", "Překladač není nakonfigurován")
            return

        self.status_callback("Překládám...", COLORS["status_working"])

        def translate_thread():
            result, error = self.translator.translate(
                input_text,
                self.source_lang,
                self.target_lang
            )
            root.after(0, lambda: self._handle_translation_result(result, error))

        threading.Thread(target=translate_thread, daemon=True).start()

    def translate_full(self, root: tk.Tk):
        """
        Kompletní překlad s GUI update (tlačítko Přeložit / Ctrl+Enter)
        """
        input_text = self.input_widget.get("1.0", tk.END).strip()

        if not input_text:
            self.status_callback("Prázdný text", COLORS["status_warning"])
            return

        if not self.translator.is_configured():
            messagebox.showerror("Chyba", "Překladač není nakonfigurován. Nastavte API klíč v nastavení.")
            return

        self.status_callback("Překládám...", COLORS["status_working"])
        root.update()

        # Překlad v separátním vlákně
        def translate_thread():
            result, error = self.translator.translate(
                input_text,
                self.source_lang,
                self.target_lang
            )

            # Aktualizace GUI v hlavním vlákně
            root.after(0, lambda: self._handle_translation_result(result, error))

        threading.Thread(target=translate_thread, daemon=True).start()

    def _handle_translation_result(self, result: Optional[str], error: Optional[str]):
        """Zpracuje výsledek překladu"""
        if error:
            self.status_callback(f"Chyba: {error}", COLORS["status_error"])
            messagebox.showerror("Chyba překladu", error)
        else:
            self.output_widget.config(state=tk.NORMAL)
            self.output_widget.delete("1.0", tk.END)
            self.output_widget.insert("1.0", result)
            self.output_widget.config(state=tk.DISABLED)

            self.status_callback("Přeloženo", COLORS["status_ready"])

            # Aktualizace usage
            self.usage_update_callback()

    def copy_translation_and_clear(self):
        """
        Zkopíruje přeložený text do schránky, vymaže input/output
        Použito ve State 2 → State 0
        """
        # Získání přeloženého textu z output pole
        translated_text = self.output_widget.get("1.0", tk.END).strip()

        if translated_text:
            # Kopírování do schránky
            pyperclip.copy(translated_text)

            # Vymazání input pole
            self.input_widget.delete("1.0", tk.END)

            # Vymazání output pole
            self.output_widget.config(state=tk.NORMAL)
            self.output_widget.delete("1.0", tk.END)
            self.output_widget.config(state=tk.DISABLED)

    def clear_all(self):
        """Vymaže textová pole"""
        self.input_widget.delete("1.0", tk.END)
        self.output_widget.config(state=tk.NORMAL)
        self.output_widget.delete("1.0", tk.END)
        self.output_widget.config(state=tk.DISABLED)
        self.status_callback("Připraveno", COLORS["text_primary"])
        self.input_widget.focus()

    def get_state(self) -> int:
        """Vrátí aktuální stav workflow"""
        return self.state

    def set_state(self, state: int):
        """Nastaví stav workflow"""
        self.state = state

    def reset_state(self):
        """Resetuje workflow do výchozího stavu"""
        self.state = self.STATE_HIDDEN
