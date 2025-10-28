# -*- coding: utf-8 -*-
"""
Transka - Desktop aplikace pro rychlý překlad
"""
import tkinter as tk
from tkinter import messagebox
import threading
import sys
import os

from transka.config import Config
from transka.deepl_translator import DeepLTranslator
from transka.google_translator import GoogleTranslator
from transka.base_translator import BaseTranslator, UsageInfo
from transka.settings_window import SettingsWindow
from transka.theme_manager import ThemeManager
from transka.translation_workflow import TranslationWorkflow
from transka.hotkey_manager import HotkeyManager
from transka.tray_manager import TrayManager
from transka.gui_builder import GUIBuilder
from transka.theme import COLORS


class TranslatorApp:
    """Hlavní aplikace pro překlad"""

    def __init__(self):
        self.config = Config()
        self.translator = self._create_translator()

        # Tkinter okno
        self.root = tk.Tk()
        self.root.title("Transka")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self._setup_window_icon()

        # Theme Manager
        self.theme_manager = ThemeManager(self.root)
        self.theme_manager.apply_theme()
        fonts = self.theme_manager.get_fonts()

        # GUI Builder
        gui_builder = GUIBuilder(
            self.root,
            fonts,
            self._get_translator_display(),
            self._get_language_display(),
            self.config.hotkey_main
        )

        # Skrytí okna při startu
        self.root.withdraw()
        self.is_visible = False

        # Build GUI
        widgets = gui_builder.build(
            on_translate=self._translate,
            on_clear=self._clear,
            on_settings=self._show_settings,
            on_close=self._hide_window
        )

        # Uložení důležitých widgetů
        self.input_text = widgets["input_text"]
        self.output_text = widgets["output_text"]
        self.status_label = widgets["status_label"]
        self.usage_label = widgets["usage_label"]
        self.translator_label = widgets["translator_label"]
        self.lang_label = widgets["lang_label"]

        # Translation Workflow Manager
        self.workflow = TranslationWorkflow(
            translator=self.translator,
            source_lang=self.config.source_lang,
            target_lang=self.config.target_lang,
            input_widget=self.input_text,
            output_widget=self.output_text,
            status_callback=self._update_status,
            usage_update_callback=self._update_usage
        )

        # Window events
        self._setup_window_events()

        # Hotkey Manager
        self.hotkey_manager = HotkeyManager(
            main_hotkey=self.config.hotkey_main,
            workflow_callback=self._handle_main_hotkey
        )
        self.hotkey_manager.register_hotkeys()

        # System Tray Manager
        self.tray_manager = TrayManager(
            app_name="Transka",
            on_show=self._show_window,
            on_settings=self._show_settings,
            on_quit=self._quit_app
        )
        self.tray_manager.start()

        # Aktualizace usage při startu
        self._update_usage()

    def _setup_window_icon(self):
        """Nastaví ikonu okna"""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "transka_icon.png")
            if os.path.exists(icon_path):
                icon_img = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Nelze načíst ikonu: {e}")

    def _create_translator(self) -> BaseTranslator:
        """Vytvoří instance překladače podle konfigurace"""
        service = self.config.translator_service.lower()
        if service == "google":
            return GoogleTranslator()
        else:
            return DeepLTranslator(self.config.api_key)

    def _get_translator_display(self) -> str:
        """Vrátí název aktivního překladače"""
        service = self.config.translator_service.upper()
        if service == "GOOGLE":
            return "🔵 Google Translate"
        else:
            return "🟢 DeepL"

    def _get_language_display(self) -> str:
        """Vrátí formátovaný string s aktuálními jazyky"""
        return f"🌐 {self.config.source_lang} → {self.config.target_lang}"

    def _setup_window_events(self):
        """Nastaví události okna"""
        self.root.protocol("WM_DELETE_WINDOW", self._hide_window)
        self.root.bind("<Escape>", lambda e: self._hide_window())
        self.root.bind("<Control-Return>", lambda e: self._translate())

    def _handle_main_hotkey(self):
        """
        Zpracuje hlavní klávesovou zkratku (3-step workflow)
        State 0 (HIDDEN) → zobraz okno → State 1 (SHOWN)
        State 1 (SHOWN) → přelož text → State 2 (TRANSLATED)
        State 2 (TRANSLATED) → zkopíruj, vymaž, zavři, restore fokus → State 0 (HIDDEN)
        """
        state = self.workflow.get_state()

        if state == TranslationWorkflow.STATE_HIDDEN:
            # Krok 1: Otevře okno
            self._show_window()
            self.workflow.set_state(TranslationWorkflow.STATE_SHOWN)

        elif state == TranslationWorkflow.STATE_SHOWN:
            # Krok 2: Přeloží text
            self.workflow.translate_with_display(self.root)
            self.workflow.set_state(TranslationWorkflow.STATE_TRANSLATED)

        elif state == TranslationWorkflow.STATE_TRANSLATED:
            # Krok 3: Zkopíruje, vymaže, zavře
            self.workflow.copy_translation_and_clear()
            self._hide_window()
            self.workflow.restore_previous_window()
            self.workflow.reset_state()

    def _show_window(self):
        """Zobrazí překladové okno a vycentruje ho na střed obrazovky"""
        if not self.is_visible:
            # Uložení předchozího okna pro restore fokus
            self.workflow.save_previous_window()

            self.root.deiconify()

            # Centrování okna
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.lift()
            self.root.focus_force()
            self.input_text.focus()
            self.is_visible = True

    def _hide_window(self):
        """Skryje překladové okno"""
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
            self.workflow.reset_state()

    def _translate(self):
        """Přeloží text (tlačítko Přeložit / Ctrl+Enter)"""
        self.workflow.translate_full(self.root)

    def _clear(self):
        """Vymaže textová pole"""
        self.workflow.clear_all()

    def _update_status(self, text: str, color: str):
        """Aktualizuje status label"""
        self.status_label.config(text=text, foreground=color)

    def _update_usage(self):
        """Aktualizuje počítadlo znaků"""
        def update_thread():
            usage_info, error = self.translator.get_usage()

            if usage_info:
                # Kontrola limitu
                if usage_info.character_count >= self.config.usage_warning_threshold:
                    color = COLORS["status_error"]
                elif usage_info.usage_percentage > 80:
                    color = COLORS["status_warning"]
                else:
                    color = COLORS["status_ready"]

                self.root.after(
                    0,
                    lambda: self.usage_label.config(
                        text=usage_info.formatted_usage,
                        foreground=color
                    )
                )

                # Varování při dosažení prahu
                if usage_info.is_near_limit:
                    self.root.after(
                        0,
                        lambda: messagebox.showwarning(
                            "Varování",
                            f"Blížíte se limitu API!\n\n{usage_info.formatted_usage}"
                        )
                    )
            elif error:
                self.root.after(
                    0,
                    lambda: self.usage_label.config(
                        text=f"Usage: {error}",
                        foreground=COLORS["status_error"]
                    )
                )

        if self.translator.is_configured():
            threading.Thread(target=update_thread, daemon=True).start()

    def _on_settings_saved(self):
        """Callback po uložení nastavení"""
        # Re-kreovat překladač
        self.translator = self._create_translator()
        self.workflow.update_translator(self.translator)
        self.workflow.update_languages(self.config.source_lang, self.config.target_lang)

        # Aktualizace GUI
        self.translator_label.config(text=self._get_translator_display())
        self.lang_label.config(text=self._get_language_display())
        self._update_usage()

    def _show_settings(self):
        """Zobrazí okno s nastavením"""
        SettingsWindow(
            self.root,
            self,
            self.config,
            self.translator,
            self._on_settings_saved
        )

    def _quit_app(self):
        """Ukončí aplikaci"""
        self.tray_manager.stop()
        self.hotkey_manager.unregister_all()
        self.root.quit()
        sys.exit(0)

    def run(self):
        """Spustí aplikaci"""
        # Kontrola API klíče při startu
        if not self.config.api_key:
            self.root.after(500, lambda: messagebox.showwarning(
                "Upozornění",
                "DeepL API klíč není nastaven.\n\nOtevřete Nastavení a zadejte API klíč."
            ))
            self.root.after(600, self._show_settings)

        self.root.mainloop()


def main():
    """Hlavní funkce aplikace"""
    app = TranslatorApp()
    app.run()


if __name__ == "__main__":
    main()
