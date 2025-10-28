# -*- coding: utf-8 -*-
"""
Okno s nastavením aplikace Transka
"""
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard

from transka.config import Config
from transka.deepl_translator import DeepLTranslator
from transka.base_translator import BaseTranslator
from transka.theme import COLORS


class SettingsWindow:
    """Okno s nastavením aplikace"""

    def __init__(self, parent, parent_app, config: Config, translator: BaseTranslator, on_save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Nastavení - Transka")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        # Dark theme pro Settings okno
        self.window.configure(bg=COLORS["bg_dark"])

        self.parent = parent_app  # Reference na TranslatorApp pro live reload
        self.config = config
        self.translator = translator
        self.on_save_callback = on_save_callback

        self._create_widgets()
        self._load_values()

        # Centrování okna
        self.window.transient(parent)
        self.window.grab_set()

    def _create_widgets(self):
        """Vytvoří widgety okna nastavení"""
        # Hlavní frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Překladová služba
        ttk.Label(main_frame, text="Překladač:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.translator_service_var = tk.StringVar()
        self.translator_service_combo = ttk.Combobox(
            main_frame,
            textvariable=self.translator_service_var,
            values=["deepl", "google"],
            state="readonly",
            width=47
        )
        self.translator_service_combo.grid(row=0, column=1, pady=5, padx=5)

        # API klíč
        ttk.Label(main_frame, text="DeepL API klíč:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=1, column=1, pady=5, padx=5)

        # Zdrojový jazyk
        ttk.Label(main_frame, text="Zdrojový jazyk:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.source_lang_var = tk.StringVar()
        self.source_lang_combo = ttk.Combobox(
            main_frame,
            textvariable=self.source_lang_var,
            values=["AUTO", "CS", "EN", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.source_lang_combo.grid(row=2, column=1, pady=5, padx=5)

        # Cílový jazyk
        ttk.Label(main_frame, text="Cílový jazyk:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.target_lang_var = tk.StringVar()
        self.target_lang_combo = ttk.Combobox(
            main_frame,
            textvariable=self.target_lang_var,
            values=["CS", "EN-US", "EN-GB", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.target_lang_combo.grid(row=3, column=1, pady=5, padx=5)

        # Klávesová zkratka
        ttk.Label(main_frame, text="Hlavní zkratka (Win+P):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.hotkey_main_entry = ttk.Entry(main_frame, width=50)
        self.hotkey_main_entry.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="", font=("", 8)).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=0)
        ttk.Label(
            main_frame,
            text="Tip: První stisk otevře okno, druhý přeloží a zkopíruje",
            font=("", 8),
            foreground="gray"
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=0, padx=5)

        # Práh varování
        ttk.Label(main_frame, text="Varování při (znacích):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.warning_threshold_entry = ttk.Entry(main_frame, width=50)
        self.warning_threshold_entry.grid(row=6, column=1, pady=5, padx=5)

        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Uložit", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test API", command=self._test_api).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zrušit", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def _load_values(self):
        """Načte aktuální hodnoty do formuláře"""
        self.translator_service_var.set(self.config.translator_service)
        self.api_key_entry.insert(0, self.config.api_key)
        self.source_lang_var.set(self.config.source_lang)
        self.target_lang_var.set(self.config.target_lang)
        self.hotkey_main_entry.insert(0, self.config.hotkey_main)
        self.warning_threshold_entry.insert(0, str(self.config.usage_warning_threshold))

    def _save_settings(self):
        """Uloží nastavení"""
        # API klíč
        new_api_key = self.api_key_entry.get().strip()
        if new_api_key != self.config.api_key:
            self.config.set_api_key(new_api_key)
            self.translator.update_api_key(new_api_key)

        # Ostatní nastavení
        self.config.set("translator_service", self.translator_service_var.get())
        self.config.set("source_lang", self.source_lang_var.get())
        self.config.set("target_lang", self.target_lang_var.get())
        self.config.set("hotkey_main", self.hotkey_main_entry.get().strip())

        try:
            threshold = int(self.warning_threshold_entry.get().strip())
            self.config.set("usage_warning_threshold", threshold)
        except ValueError:
            messagebox.showerror("Chyba", "Neplatná hodnota pro práh varování")
            return

        # Okamžitá aplikace změn bez restartu
        old_hotkey = self.config.hotkey_main
        new_hotkey = self.hotkey_main_entry.get().strip()

        # Pokud se změnila zkratka, re-registruj ji
        if old_hotkey != new_hotkey:
            try:
                keyboard.remove_hotkey(old_hotkey)
            except:
                pass
            try:
                keyboard.add_hotkey(new_hotkey, self.parent._handle_main_hotkey)
            except Exception as e:
                messagebox.showerror("Chyba", f"Nelze nastavit zkratku {new_hotkey}: {e}")
                return

        messagebox.showinfo("Úspěch", "Nastavení aplikováno okamžitě!")
        self.on_save_callback()
        self.window.destroy()

    def _test_api(self):
        """Test připojení k DeepL API"""
        new_api_key = self.api_key_entry.get().strip()

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
