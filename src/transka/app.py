# -*- coding: utf-8 -*-
"""
Transka - Desktop aplikace pro rychlý překlad
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font as tkfont
import threading
import pyperclip
import keyboard
import pystray
from PIL import Image, ImageDraw
from typing import Optional
import sys
import os

from transka.config import Config
from transka.deepl_translator import DeepLTranslator
from transka.google_translator import GoogleTranslator
from transka.base_translator import BaseTranslator, UsageInfo
from transka.theme import COLORS, FONTS


class SettingsWindow:
    """Okno s nastavením aplikace"""

    def __init__(self, parent, parent_app, config: Config, translator: DeepLTranslator, on_save_callback):
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


class TranslatorApp:
    """Hlavní aplikace pro překlad"""

    def __init__(self):
        self.config = Config()
        self.translator = self._create_translator()

        self.root = tk.Tk()
        self.root.title("Transka")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")

        # Nastavení ikony okna
        try:
            # Cesta k ikoně v assets/
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "transka_icon.png")
            if os.path.exists(icon_path):
                icon_img = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Nelze načíst ikonu: {e}")

        # Modern Dark Theme
        self._apply_theme()

        # Skrytí okna při startu
        self.root.withdraw()

        # Proměnné
        self.is_visible = False
        self.previous_window = None
        # State machine pro workflow:
        # 0 = HIDDEN (skryté), 1 = SHOWN (viditelné), 2 = TRANSLATED (přeloženo)
        self.window_state = 0

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

    def _create_translator(self) -> BaseTranslator:
        """Vytvoří instance překladače podle konfigurace"""
        service = self.config.translator_service.lower()

        if service == "google":
            return GoogleTranslator()
        else:  # default: deepl
            return DeepLTranslator(self.config.api_key)

    def _get_translator_display(self) -> str:
        """Vrátí název aktivního překladače"""
        service = self.config.translator_service.upper()
        if service == "GOOGLE":
            return "🔵 Google Translate"
        else:  # DEEPL
            return "🟢 DeepL"

    def _get_language_display(self) -> str:
        """Vrátí formátovaný string s aktuálními jazyky"""
        source = self.config.source_lang
        target = self.config.target_lang
        return f"🌐 {source} → {target}"

    def _apply_theme(self):
        """Aplikuje modern dark theme s glow efekty"""
        # Pozadí hlavního okna
        self.root.configure(bg=COLORS["bg_dark"])

        # Dark titlebar pro Windows 11/10 (odstranění bílého pruhu nahoře)
        try:
            # Musíme počkat, než se okno vytvoří
            self.root.update_idletasks()

            import ctypes
            # Získání HWND handle přímo z winfo_id()
            hwnd = self.root.winfo_id()

            # DWMWA_USE_IMMERSIVE_DARK_MODE = 20 (Windows 11)
            # DWMWA_USE_IMMERSIVE_DARK_MODE = 19 (Windows 10 build 19041+)
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            value = ctypes.c_int(2)  # 2 = force dark mode, 1 = enable

            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
        except Exception as e:
            print(f"Dark titlebar nepodporován: {e}")  # Debug info

        # Vytvoření Fira Code fontu
        try:
            self.mono_font = tkfont.Font(family="Fira Code", size=FONTS["size_normal"])
            self.mono_font_large = tkfont.Font(family="Fira Code", size=FONTS["size_large"])
        except:
            # Fallback na Consolas pokud Fira Code není k dispozici
            self.mono_font = tkfont.Font(family="Consolas", size=FONTS["size_normal"])
            self.mono_font_large = tkfont.Font(family="Consolas", size=FONTS["size_large"])

        self.sans_font = tkfont.Font(family="Segoe UI", size=FONTS["size_normal"])
        self.sans_font_bold = tkfont.Font(family="Segoe UI", size=FONTS["size_normal"], weight="bold")

        # TTK Style pro dark theme
        style = ttk.Style()
        style.theme_use('clam')  # Používáme 'clam' theme jako základ

        # Frame style
        style.configure('TFrame', background=COLORS["bg_dark"])

        # Label style
        style.configure('TLabel',
            background=COLORS["bg_dark"],
            foreground=COLORS["text_primary"],
            font=self.sans_font
        )

        # Button style s glow efektem
        style.configure('TButton',
            background=COLORS["bg_button"],
            foreground=COLORS["accent_cyan"],
            bordercolor=COLORS["border"],
            focuscolor=COLORS["border_focus"],
            font=self.sans_font_bold,
            relief=tk.FLAT
        )
        style.map('TButton',
            background=[('active', COLORS["bg_button_hover"]), ('pressed', COLORS["bg_darker"])],
            foreground=[('active', COLORS["accent_cyan"]), ('pressed', COLORS["accent_purple"])]
        )

        # Entry style
        style.configure('TEntry',
            fieldbackground=COLORS["bg_input"],
            background=COLORS["bg_input"],
            foreground=COLORS["text_primary"],
            insertcolor=COLORS["accent_cyan"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border_focus"],
            darkcolor=COLORS["border"]
        )

        # Combobox style
        style.configure('TCombobox',
            fieldbackground=COLORS["bg_input"],
            background=COLORS["bg_button"],
            foreground=COLORS["text_primary"],
            arrowcolor=COLORS["accent_cyan"],
            bordercolor=COLORS["border"]
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', COLORS["bg_input"])],
            selectbackground=[('readonly', COLORS["accent_cyan"])],
            selectforeground=[('readonly', COLORS["bg_dark"])]
        )

    def _create_widgets(self):
        """Vytvoří GUI komponenty"""
        # Hlavní frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfigurace grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Header s aktuálními jazyky a překladačem
        # Použití tk.Frame místo ttk.Frame pro správné dark pozadí
        header_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Použití tk.Label místo ttk.Label pro přesné barvy
        self.translator_label = tk.Label(
            header_frame,
            text=self._get_translator_display(),
            fg=COLORS["accent_yellow"],
            bg=COLORS["bg_dark"],
            font=self.sans_font_bold
        )
        self.translator_label.pack(side=tk.LEFT, padx=(0, 15))

        self.lang_label = tk.Label(
            header_frame,
            text=self._get_language_display(),
            fg=COLORS["accent_cyan"],
            bg=COLORS["bg_dark"],
            font=self.sans_font_bold
        )
        self.lang_label.pack(side=tk.LEFT)

        # Input label a textové pole
        input_label = ttk.Label(main_frame, text="Text k překladu:")
        input_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            wrap=tk.WORD,
            font=self.mono_font_large,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],  # Kurzor
            selectbackground=COLORS["accent_cyan"],
            selectforeground=COLORS["bg_dark"],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=COLORS["border_focus"],
            highlightbackground=COLORS["border"]
        )
        self.input_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        # Styling scrollbaru - dark theme
        self.input_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            width=12
        )
        self.input_text.focus()

        # Output label a textové pole
        output_label = ttk.Label(main_frame, text="Přeložený text:")
        output_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))

        self.output_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=self.mono_font_large,
            bg=COLORS["bg_darker"],
            fg=COLORS["text_primary"],
            selectbackground=COLORS["accent_purple"],
            selectforeground=COLORS["bg_dark"],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=2,
            highlightcolor=COLORS["accent_purple"],
            highlightbackground=COLORS["border"]
        )
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        # Styling scrollbaru - dark theme
        self.output_text.vbar.config(
            bg=COLORS["bg_darker"],
            troughcolor=COLORS["bg_dark"],
            activebackground=COLORS["accent_purple"],
            relief=tk.FLAT,
            width=12
        )

        # Status bar s počítadlem znaků
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        self.status_label = ttk.Label(status_frame, text="Připraveno", foreground=COLORS["text_primary"])
        self.status_label.pack(side=tk.LEFT)

        self.usage_label = ttk.Label(status_frame, text="Načítám usage...", foreground=COLORS["text_secondary"])
        self.usage_label.pack(side=tk.RIGHT)

        # Tlačítka
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=(10, 0))

        ttk.Button(
            button_frame,
            text=f"Přeložit ({self.config.hotkey_main})",
            command=self._translate
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="Vymazat", command=self._clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Nastavení", command=self._show_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Zavřít", command=self._hide_window).pack(side=tk.LEFT, padx=5)

    def _setup_window_events(self):
        """Nastaví události okna"""
        self.root.protocol("WM_DELETE_WINDOW", self._hide_window)

        # ESC pro zavření okna
        self.root.bind("<Escape>", lambda e: self._hide_window())

        # Ctrl+Return pro překlad v rámci okna
        self.root.bind("<Control-Return>", lambda e: self._translate())

        # Ctrl+P+P (dvojité stisknutí) jako alternativa k Win+P
        self._last_ctrl_p_time = 0
        self.root.bind("<Control-p>", self._handle_ctrl_p_double)

    def _handle_ctrl_p_double(self, event):
        """Zpracuje Ctrl+P+P (dvojité stisknutí rychle za sebou)"""
        import time
        current_time = time.time()

        # Pokud mezi stisky je méně než 0.5s, považuj za dvojité stisknutí
        if current_time - self._last_ctrl_p_time < 0.5:
            # Dvojité stisknutí! Stejná funkce jako Win+P
            self._handle_main_hotkey()
            self._last_ctrl_p_time = 0  # Reset
        else:
            # První stisknutí, zapamatuj čas
            self._last_ctrl_p_time = current_time

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

        self.tray_icon = pystray.Icon("transka", create_image(), "Transka", menu)

        # Spuštění tray ikony v separátním vlákně
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

    def _setup_hotkeys(self):
        """Nastaví globální klávesové zkratky"""
        try:
            # Jediná zkratka Win+P pro vše:
            # - Pokud okno není viditelné → zobrazí se
            # - Pokud okno je viditelné → přeloží a zkopíruje do schránky
            keyboard.add_hotkey(self.config.hotkey_main, self._handle_main_hotkey)

        except Exception as e:
            print(f"Chyba při nastavování zkratek: {e}")

    def _handle_main_hotkey(self):
        """
        Zpracuje hlavní klávesovou zkratku Win+P (nebo Ctrl+P+P)

        State machine workflow:
        State 0 (HIDDEN) → zobraz okno → State 1 (SHOWN)
        State 1 (SHOWN) → přelož text → State 2 (TRANSLATED)
        State 2 (TRANSLATED) → zkopíruj, vymaž, zavři, restore fokus → State 0 (HIDDEN)
        """
        if self.window_state == 0:  # HIDDEN
            # 1. Ctrl+P+P: Otevře okno
            self._show_window()
            self.window_state = 1
        elif self.window_state == 1:  # SHOWN
            # 2. Ctrl+P+P: Přeloží text a zobrazí v okně
            self._translate_only()
            self.window_state = 2
        elif self.window_state == 2:  # TRANSLATED
            # 3. Ctrl+P+P: Zkopíruje, vymaže, zavře, restore fokus
            self._copy_and_close()
            self.window_state = 0

    def _show_window(self):
        """Zobrazí překladové okno a vycentruje ho na střed obrazovky"""
        if not self.is_visible:
            # Uložení předchozího okna pro restore fokus
            try:
                import ctypes
                self.previous_window = ctypes.windll.user32.GetForegroundWindow()
            except:
                self.previous_window = None

            self.root.deiconify()

            # Centrování okna na střed obrazovky
            self.root.update_idletasks()  # Aktualizace geometrie
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Výpočet pozice pro střed
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            self.root.lift()
            self.root.focus_force()
            self.input_text.focus()
            self.is_visible = True

    def _hide_window(self):
        """Skryje překladové okno a resetuje state"""
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
            self.window_state = 0  # Reset do HIDDEN state

    def _translate(self):
        """Přeloží text"""
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            self.status_label.config(text="Prázdný text", foreground=COLORS["status_warning"])
            return

        if not self.translator.is_configured():
            messagebox.showerror("Chyba", "DeepL API není nakonfigurováno. Nastavte API klíč v nastavení.")
            return

        self.status_label.config(text="Překládám...", foreground=COLORS["status_working"])
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
            self.status_label.config(text=f"Chyba: {error}", foreground=COLORS["status_error"])
            messagebox.showerror("Chyba překladu", error)
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state=tk.DISABLED)

            self.status_label.config(text="Přeloženo", foreground=COLORS["status_ready"])

            # Aktualizace usage
            self._update_usage()

    def _translate_only(self):
        """
        Přeloží text a zobrazí v output poli (NEUZAVŘE okno, NEKOPÍRUJE)
        Použito ve State 1 → State 2
        """
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            return

        if not self.translator.is_configured():
            messagebox.showerror("Chyba", "Překladač není nakonfigurován")
            return

        self.status_label.config(text="Překládám...", foreground=COLORS["status_working"])

        def translate_thread():
            result, error = self.translator.translate(
                input_text,
                self.config.source_lang,
                self.config.target_lang
            )
            self.root.after(0, lambda: self._handle_translation_result(result, error))

        threading.Thread(target=translate_thread, daemon=True).start()

    def _copy_and_close(self):
        """
        Zkopíruje přeložený text do schránky, vymaže input, zavře okno a restore fokus
        Použito ve State 2 → State 0
        """
        # Získání přeloženého textu z output pole
        translated_text = self.output_text.get("1.0", tk.END).strip()

        if translated_text:
            # Kopírování do schránky
            pyperclip.copy(translated_text)

            # Vymazání input pole
            self.input_text.delete("1.0", tk.END)

            # Vymazání output pole
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.config(state=tk.DISABLED)

            # Skrytí okna (resetuje window_state na 0)
            self._hide_window()

            # Restore fokus na předchozí okno
            if self.previous_window:
                try:
                    import ctypes
                    ctypes.windll.user32.SetForegroundWindow(self.previous_window)
                except:
                    pass

    def _translate_and_copy(self):
        """
        LEGACY: Přeloží text a zkopíruje do schránky (stará logika)
        Používá se pro tlačítko "Přeložit" a Ctrl+Enter
        Také resetuje window_state pro konzistenci
        """
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

            # Vymazání input pole po úspěšném překladu
            self.root.after(50, self._clear_input_only)

            # Skrytí okna (automaticky resetuje window_state na 0)
            self.root.after(100, self._hide_window)

    def _clear_input_only(self):
        """Vymaže pouze input pole (pro automatické vymazání po překladu)"""
        self.input_text.delete("1.0", tk.END)

    def _clear(self):
        """Vymaže textová pole"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_label.config(text="Připraveno", foreground=COLORS["text_primary"])
        self.input_text.focus()

    def _update_usage(self):
        """Aktualizuje počítadlo znaků"""
        def update_thread():
            usage_info, error = self.translator.get_usage()

            if usage_info:
                # Kontrola, zda se blížíme limitu
                if usage_info.character_count >= self.config.usage_warning_threshold:
                    color = COLORS["status_error"]  # Červená
                elif usage_info.usage_percentage > 80:
                    color = COLORS["status_warning"]  # Oranžová
                else:
                    color = COLORS["status_ready"]  # Zelená

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
                    lambda: self.usage_label.config(text=f"Usage: {error}", foreground=COLORS["status_error"])
                )

        if self.translator.is_configured():
            threading.Thread(target=update_thread, daemon=True).start()

    def _on_settings_saved(self):
        """Callback po uložení nastavení - aktualizuje GUI"""
        # Re-kreovat překladač při změně služby
        self.translator = self._create_translator()
        # Aktualizace zobrazení překladače
        self.translator_label.config(text=self._get_translator_display())
        # Aktualizace zobrazení jazyků
        self.lang_label.config(text=self._get_language_display())
        # Aktualizace usage
        self._update_usage()

    def _show_settings(self):
        """Zobrazí okno s nastavením"""
        SettingsWindow(self.root, self, self.config, self.translator, self._on_settings_saved)

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
