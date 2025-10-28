"""
DeepL Translator - Desktop aplikace pro rychlý překlad
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import pyperclip
import keyboard
import pystray
from PIL import Image, ImageDraw
from typing import Optional
import sys

from src.config import Config
from src.deepl_translator import DeepLTranslator
from src.base_translator import UsageInfo


class SettingsWindow:
    """Okno s nastavením aplikace"""

    def __init__(self, parent, config: Config, translator: DeepLTranslator, on_save_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Nastavení")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

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

        # API klíč
        ttk.Label(main_frame, text="DeepL API klíč:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, pady=5, padx=5)

        # Zdrojový jazyk
        ttk.Label(main_frame, text="Zdrojový jazyk:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.source_lang_var = tk.StringVar()
        self.source_lang_combo = ttk.Combobox(
            main_frame,
            textvariable=self.source_lang_var,
            values=["AUTO", "CS", "EN", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.source_lang_combo.grid(row=1, column=1, pady=5, padx=5)

        # Cílový jazyk
        ttk.Label(main_frame, text="Cílový jazyk:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.target_lang_var = tk.StringVar()
        self.target_lang_combo = ttk.Combobox(
            main_frame,
            textvariable=self.target_lang_var,
            values=["CS", "EN-US", "EN-GB", "DE", "FR", "ES", "IT", "PL", "RU"],
            state="readonly",
            width=47
        )
        self.target_lang_combo.grid(row=2, column=1, pady=5, padx=5)

        # Klávesové zkratky
        ttk.Label(main_frame, text="Zkratka pro otevření:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.hotkey_show_entry = ttk.Entry(main_frame, width=50)
        self.hotkey_show_entry.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(main_frame, text="Zkratka pro překlad:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.hotkey_translate_entry = ttk.Entry(main_frame, width=50)
        self.hotkey_translate_entry.grid(row=4, column=1, pady=5, padx=5)

        # Práh varování
        ttk.Label(main_frame, text="Varování při (znacích):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.warning_threshold_entry = ttk.Entry(main_frame, width=50)
        self.warning_threshold_entry.grid(row=5, column=1, pady=5, padx=5)

        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Uložit", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test API", command=self._test_api).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zrušit", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def _load_values(self):
        """Načte aktuální hodnoty do formuláře"""
        self.api_key_entry.insert(0, self.config.api_key)
        self.source_lang_var.set(self.config.source_lang)
        self.target_lang_var.set(self.config.target_lang)
        self.hotkey_show_entry.insert(0, self.config.hotkey_show)
        self.hotkey_translate_entry.insert(0, self.config.hotkey_translate)
        self.warning_threshold_entry.insert(0, str(self.config.usage_warning_threshold))

    def _save_settings(self):
        """Uloží nastavení"""
        # API klíč
        new_api_key = self.api_key_entry.get().strip()
        if new_api_key != self.config.api_key:
            self.config.set_api_key(new_api_key)
            self.translator.update_api_key(new_api_key)

        # Ostatní nastavení
        self.config.set("source_lang", self.source_lang_var.get())
        self.config.set("target_lang", self.target_lang_var.get())
        self.config.set("hotkey_show", self.hotkey_show_entry.get().strip())
        self.config.set("hotkey_translate", self.hotkey_translate_entry.get().strip())

        try:
            threshold = int(self.warning_threshold_entry.get().strip())
            self.config.set("usage_warning_threshold", threshold)
        except ValueError:
            messagebox.showerror("Chyba", "Neplatná hodnota pro práh varování")
            return

        messagebox.showinfo("Úspěch", "Nastavení uloženo. Restartujte aplikaci pro aplikování zkratek.")
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


class TranslatorApp:
    """Hlavní aplikace pro překlad"""

    def __init__(self):
        self.config = Config()
        self.translator = DeepLTranslator(self.config.api_key)

        self.root = tk.Tk()
        self.root.title("DeepL Translator")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")

        # Skrytí okna při startu
        self.root.withdraw()

        # Proměnné
        self.is_visible = False
        self.previous_window = None

        # GUI komponenty
        self._create_widgets()
        self._setup_window_events()

        # System tray
        self.tray_icon: Optional[pystray.Icon] = None
        self._setup_tray()

        # Klávesové zkratky
        self._setup_hotkeys()

        # Aktualizace usage při startu
        self._update_usage()

    def _create_widgets(self):
        """Vytvoří GUI komponenty"""
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfigurace grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Input label a textové pole
        ttk.Label(main_frame, text="Text k překladu:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.input_text.focus()

        # Output label a textové pole
        ttk.Label(main_frame, text="Přeložený text:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Status bar s počítadlem znaků
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        self.status_label = ttk.Label(status_frame, text="Připraveno")
        self.status_label.pack(side=tk.LEFT)

        self.usage_label = ttk.Label(status_frame, text="Načítám usage...", foreground="gray")
        self.usage_label.pack(side=tk.RIGHT)

        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, pady=(10, 0))

        ttk.Button(
            button_frame,
            text=f"Přeložit ({self.config.hotkey_translate})",
            command=self._translate
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Vymazat", command=self._clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Nastavení", command=self._show_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zavřít", command=self._hide_window).pack(side=tk.LEFT, padx=5)

    def _setup_window_events(self):
        """Nastaví události okna"""
        self.root.protocol("WM_DELETE_WINDOW", self._hide_window)

        # Bind pro Win+P v rámci okna
        self.root.bind("<Control-Return>", lambda e: self._translate())

    def _setup_tray(self):
        """Nastaví system tray ikonu"""
        # Vytvoření jednoduché ikony
        def create_image():
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), color=(33, 150, 243))
            dc = ImageDraw.Draw(image)
            dc.rectangle([width // 4, height // 4, width * 3 // 4, height * 3 // 4], fill=(255, 255, 255))
            return image

        # Menu pro tray
        menu = pystray.Menu(
            pystray.MenuItem("Zobrazit", self._show_window),
            pystray.MenuItem("Nastavení", self._show_settings),
            pystray.MenuItem("Ukončit", self._quit_app)
        )

        self.tray_icon = pystray.Icon("deepl_translator", create_image(), "DeepL Translator", menu)

        # Spuštění tray ikony v separátním vlákně
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

    def _setup_hotkeys(self):
        """Nastaví globální klávesové zkratky"""
        try:
            # Zkratka pro zobrazení okna
            keyboard.add_hotkey(self.config.hotkey_show, self._show_window)

            # Zkratka pro překlad
            keyboard.add_hotkey(self.config.hotkey_translate, self._translate_and_copy)

        except Exception as e:
            print(f"Chyba při nastavování zkratek: {e}")

    def _show_window(self):
        """Zobrazí překladové okno"""
        if not self.is_visible:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.input_text.focus()
            self.is_visible = True

    def _hide_window(self):
        """Skryje překladové okno"""
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False

    def _translate(self):
        """Přeloží text"""
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            self.status_label.config(text="Prázdný text", foreground="orange")
            return

        if not self.translator.is_configured():
            messagebox.showerror("Chyba", "DeepL API není nakonfigurováno. Nastavte API klíč v nastavení.")
            return

        self.status_label.config(text="Překládám...", foreground="blue")
        self.root.update()

        # Překlad v separátním vlákně
        def translate_thread():
            result, error = self.translator.translate(
                input_text,
                self.config.source_lang,
                self.config.target_lang
            )

            # Aktualizace GUI v hlavním vlákně
            self.root.after(0, lambda: self._handle_translation_result(result, error))

        threading.Thread(target=translate_thread, daemon=True).start()

    def _handle_translation_result(self, result: Optional[str], error: Optional[str]):
        """Zpracuje výsledek překladu"""
        if error:
            self.status_label.config(text=f"Chyba: {error}", foreground="red")
            messagebox.showerror("Chyba překladu", error)
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state=tk.DISABLED)

            self.status_label.config(text="Přeloženo", foreground="green")

            # Aktualizace usage
            self._update_usage()

    def _translate_and_copy(self):
        """Přeloží text a zkopíruje do schránky"""
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            return

        if not self.translator.is_configured():
            return

        # Překlad
        result, error = self.translator.translate(
            input_text,
            self.config.source_lang,
            self.config.target_lang
        )

        if result and not error:
            # Kopírování do schránky
            pyperclip.copy(result)

            # Aktualizace GUI
            self.root.after(0, lambda: self._handle_translation_result(result, error))

            # Skrytí okna
            self.root.after(100, self._hide_window)

    def _clear(self):
        """Vymaže textová pole"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_label.config(text="Připraveno", foreground="black")
        self.input_text.focus()

    def _update_usage(self):
        """Aktualizuje počítadlo znaků"""
        def update_thread():
            usage_info, error = self.translator.get_usage()

            if usage_info:
                # Kontrola, zda se blížíme limitu
                if usage_info.character_count >= self.config.usage_warning_threshold:
                    color = "red"
                elif usage_info.usage_percentage > 80:
                    color = "orange"
                else:
                    color = "green"

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
                    lambda: self.usage_label.config(text=f"Usage: {error}", foreground="red")
                )

        if self.translator.is_configured():
            threading.Thread(target=update_thread, daemon=True).start()

    def _show_settings(self):
        """Zobrazí okno s nastavením"""
        SettingsWindow(self.root, self.config, self.translator, self._update_usage)

    def _quit_app(self):
        """Ukončí aplikaci"""
        if self.tray_icon:
            self.tray_icon.stop()
        keyboard.unhook_all()
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
