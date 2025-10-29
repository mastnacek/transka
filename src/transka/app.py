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
from transka.theme_manager import ThemeManager
from transka.translation_workflow import TranslationWorkflow
from transka.hotkey_manager import HotkeyManager
from transka.tray_manager import TrayManager
from transka.gui_builder_v2 import GUIBuilderV2
from transka.theme import COLORS


class TranslatorApp:
    """Hlavní aplikace pro překlad"""

    def __init__(self):
        self.config = Config()
        self.translator = self._create_translator()

        # Tkinter okno
        self.root = tk.Tk()
        self.root.title("Transka")
        # Větší okno pro tabs
        self.root.geometry("750x600")
        self._setup_window_icon()

        # Theme Manager
        self.theme_manager = ThemeManager(self.root)
        self.theme_manager.apply_theme()
        fonts = self.theme_manager.get_fonts()

        # GUI Builder V2 (s tabs)
        self.gui_builder = GUIBuilderV2(
            self.root,
            fonts,
            self._get_translator_display(),
            self._get_language_display(),
            self.config.hotkey_main,
            self.config,
            self.translator,
            parent_app=self
        )

        # Skrytí okna při startu
        self.root.withdraw()
        self.is_visible = False

        # Build GUI
        widgets = self.gui_builder.build(
            on_translate=self._translate,
            on_clear=self._clear,
            on_save_settings=self._save_settings,
            on_test_api=self._test_api,
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
            swap_hotkey=self.config.hotkey_swap,
            clear_hotkey=self.config.hotkey_clear,
            workflow_callback=self._handle_main_hotkey,
            swap_callback=self._swap_languages,
            clear_callback=self._clear_input
        )
        self.hotkey_manager.register_hotkeys()

        # System Tray Manager
        self.tray_manager = TrayManager(
            app_name="Transka",
            on_show=self._show_window,
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

        # Keyboard shortcuts pro tab switching
        self.root.bind("<Control-Key-1>", lambda e: self.gui_builder.switch_to_translation_tab())
        self.root.bind("<Control-Key-2>", lambda e: self.gui_builder.switch_to_settings_tab())

    def _handle_main_hotkey(self):
        """
        Zpracuje hlavní klávesovou zkratku (3-step workflow s smart detection)

        State 0 (HIDDEN) → zobraz okno → State 1 (SHOWN)
        State 1 (SHOWN):
          - JE přeložený text v output? → zkopíruj a zavři (skip překladu)
          - NENÍ přeložený text? → přelož text → State 2 (TRANSLATED)
        State 2 (TRANSLATED) → zkopíruj, vymaž, zavři, restore fokus → State 0 (HIDDEN)
        """
        state = self.workflow.get_state()

        if state == TranslationWorkflow.STATE_HIDDEN:
            # Krok 1: Otevře okno (vždy na Translation tab)
            self._show_window()
            self.gui_builder.switch_to_translation_tab()  # Force Translation tab
            self.workflow.set_state(TranslationWorkflow.STATE_SHOWN)

        elif state == TranslationWorkflow.STATE_SHOWN:
            # Smart detection: Pokud už existuje přeložený text (např. z Ctrl+Enter),
            # přeskoč překlad a rovnou zkopíruj + zavři
            translated_text = self.output_text.get("1.0", "end-1c").strip()

            if translated_text:
                # Existuje přeložený text → zkopíruj a zavři (jako krok 3)
                self.workflow.copy_translation_and_clear()
                self._hide_window()
                self.workflow.restore_previous_window()
                self.workflow.reset_state()
            else:
                # Žádný přeložený text → normální překlad (krok 2)
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

    def _swap_languages(self):
        """Prohodí zdrojový a cílový jazyk (Ctrl+S+S)"""
        # Swap jazyků v config
        old_source = self.config.source_lang
        old_target = self.config.target_lang

        self.config.set("source_lang", old_target)
        self.config.set("target_lang", old_source)

        # Aktualizace workflow
        self.workflow.update_languages(self.config.source_lang, self.config.target_lang)

        # Aktualizace GUI label
        self.lang_label.config(text=self._get_language_display())

        # Zobrazení notifikace
        self._update_status(
            f"🔄 Směr změněn: {self.config.source_lang} → {self.config.target_lang}",
            COLORS["status_ready"]
        )

    def _clear_input(self):
        """Vymaže pouze input pole (Ctrl+C+C)"""
        # Vymaže input pole
        self.input_text.delete("1.0", "end")

        # Fokus na input pole (pokud je okno viditelné)
        if self.is_visible:
            self.input_text.focus()

        # Zobrazení notifikace
        self._update_status(
            "🗑️ Input pole vymazáno",
            COLORS["status_ready"]
        )

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

    def _save_settings(self):
        """Uloží nastavení z Settings tab"""
        settings = self.gui_builder.get_settings_values()

        # API klíč
        new_api_key = settings["api_key"]
        if new_api_key != self.config.api_key:
            self.config.set_api_key(new_api_key)
            self.translator.update_api_key(new_api_key)

        # Ostatní nastavení
        self.config.set("translator_service", settings["translator_service"])
        self.config.set("source_lang", settings["source_lang"])
        self.config.set("target_lang", settings["target_lang"])
        self.config.set("hotkey_main", settings["hotkey_main"])
        self.config.set("hotkey_swap", settings["hotkey_swap"])
        self.config.set("hotkey_clear", settings["hotkey_clear"])

        try:
            threshold = int(settings["usage_warning_threshold"])
            self.config.set("usage_warning_threshold", threshold)
        except ValueError:
            messagebox.showerror("Chyba", "Neplatná hodnota pro práh varování")
            return

        # Okamžitá aplikace změn - hlavní zkratka
        old_main_hotkey = self.config.hotkey_main
        new_main_hotkey = settings["hotkey_main"]

        if old_main_hotkey != new_main_hotkey:
            success = self.hotkey_manager.update_main_hotkey(new_main_hotkey)
            if not success:
                messagebox.showerror("Chyba", f"Nelze nastavit hlavní zkratku {new_main_hotkey}")
                return

        # Okamžitá aplikace změn - swap zkratka
        old_swap_hotkey = self.config.hotkey_swap
        new_swap_hotkey = settings["hotkey_swap"]

        if old_swap_hotkey != new_swap_hotkey:
            success = self.hotkey_manager.update_swap_hotkey(new_swap_hotkey)
            if not success:
                messagebox.showerror("Chyba", f"Nelze nastavit swap zkratku {new_swap_hotkey}")
                return

        # Okamžitá aplikace změn - clear zkratka
        old_clear_hotkey = self.config.hotkey_clear
        new_clear_hotkey = settings["hotkey_clear"]

        if old_clear_hotkey != new_clear_hotkey:
            success = self.hotkey_manager.update_clear_hotkey(new_clear_hotkey)
            if not success:
                messagebox.showerror("Chyba", f"Nelze nastavit clear zkratku {new_clear_hotkey}")
                return

        messagebox.showinfo("Úspěch", "Nastavení aplikováno okamžitě!")
        self._on_settings_saved()

    def _test_api(self):
        """Test připojení k DeepL API"""
        settings = self.gui_builder.get_settings_values()
        new_api_key = settings["api_key"]

        if not new_api_key:
            messagebox.showerror("Chyba", "Zadejte API klíč")
            return

        # Dočasný translator pro test
        test_translator = DeepLTranslator(new_api_key)

        if not test_translator.is_configured():
            messagebox.showerror("Chyba", "Nepodařilo se inicializovat DeepL API")
            return

        # Test překladu
        result, error = test_translator.translate("Ahoj", "CS", "EN-US")

        if error:
            messagebox.showerror("Chyba API", f"Test selhal:\n{error}")
        else:
            usage_info, usage_error = test_translator.get_usage()
            if usage_info:
                messagebox.showinfo(
                    "Úspěch",
                    f"API klíč funguje!\n\n"
                    f"Test překladu: Ahoj → {result}\n\n"
                    f"Spotřeba: {usage_info.formatted_usage}"
                )
            else:
                messagebox.showinfo("Úspěch", f"API klíč funguje!\n\nTest překladu: Ahoj → {result}")

    def _show_settings_tab(self):
        """Zobrazí okno s Settings tabem"""
        self._show_window()
        self.gui_builder.switch_to_settings_tab()

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
            self.root.after(600, self._show_settings_tab)

        self.root.mainloop()


def main():
    """Hlavní funkce aplikace"""
    app = TranslatorApp()
    app.run()


if __name__ == "__main__":
    main()
