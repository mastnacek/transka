# -*- coding: utf-8 -*-
"""
Hotkey Manager pro aplikaci Transka
Spravuje globální klávesové zkratky včetně dvojitého stisku
"""
import keyboard
import time
from typing import Callable


class HotkeyManager:
    """Správce globálních klávesových zkratek"""

    def __init__(
        self,
        main_hotkey: str,
        swap_hotkey: str,
        workflow_callback: Callable[[], None],
        swap_callback: Callable[[], None]
    ):
        """
        Inicializuje HotkeyManager

        Args:
            main_hotkey: Hlavní zkratka (např. "win+p")
            swap_hotkey: Zkratka pro swap jazyků (např. "ctrl+s")
            workflow_callback: Callback funkce pro zpracování workflow hotkey
            swap_callback: Callback funkce pro swap jazyků
        """
        self.main_hotkey = main_hotkey
        self.swap_hotkey = swap_hotkey
        self.workflow_callback = workflow_callback
        self.swap_callback = swap_callback
        self._last_ctrl_p_time = 0
        self._last_swap_time = 0
        self._registered_hotkeys = []

    def register_hotkeys(self):
        """Zaregistruje všechny globální klávesové zkratky"""
        try:
            # Hlavní zkratka (výchozí: Ctrl+P pro double-press detection)
            keyboard.add_hotkey(self.main_hotkey, self._handle_ctrl_p)
            self._registered_hotkeys.append(self.main_hotkey)

            # Swap jazyků zkratka (výchozí: Ctrl+S pro double-press detection)
            keyboard.add_hotkey(self.swap_hotkey, self._handle_swap)
            self._registered_hotkeys.append(self.swap_hotkey)

        except Exception as e:
            print(f"Chyba při nastavování zkratek: {e}")

    def _handle_ctrl_p(self):
        """Globální handler pro hlavní zkratku (double-press detection)"""
        current_time = time.time()
        if current_time - self._last_ctrl_p_time < 0.5:
            # Dvojité stisknutí < 0.5s
            self.workflow_callback()
            self._last_ctrl_p_time = 0
        else:
            # První stisknutí
            self._last_ctrl_p_time = current_time

    def _handle_swap(self):
        """Globální handler pro swap zkratku (double-press detection)"""
        current_time = time.time()
        if current_time - self._last_swap_time < 0.5:
            # Dvojité stisknutí < 0.5s
            self.swap_callback()
            self._last_swap_time = 0
        else:
            # První stisknutí
            self._last_swap_time = current_time

    def update_main_hotkey(self, new_hotkey: str):
        """
        Aktualizuje hlavní zkratku (pro live reload z Settings)

        Args:
            new_hotkey: Nová zkratka (např. "ctrl+shift+t")

        Returns:
            bool: True pokud úspěšné, False při chybě
        """
        try:
            # Odstranit starou zkratku
            if self.main_hotkey in self._registered_hotkeys:
                keyboard.remove_hotkey(self.main_hotkey)
                self._registered_hotkeys.remove(self.main_hotkey)

            # Přidat novou zkratku s double-press detekcí
            keyboard.add_hotkey(new_hotkey, self._handle_ctrl_p)
            self._registered_hotkeys.append(new_hotkey)
            self.main_hotkey = new_hotkey
            return True
        except Exception as e:
            print(f"Chyba při změně zkratky: {e}")
            return False

    def update_swap_hotkey(self, new_hotkey: str):
        """
        Aktualizuje swap zkratku (pro live reload z Settings)

        Args:
            new_hotkey: Nová zkratka (např. "ctrl+d")

        Returns:
            bool: True pokud úspěšné, False při chybě
        """
        try:
            # Odstranit starou zkratku
            if self.swap_hotkey in self._registered_hotkeys:
                keyboard.remove_hotkey(self.swap_hotkey)
                self._registered_hotkeys.remove(self.swap_hotkey)

            # Přidat novou zkratku
            keyboard.add_hotkey(new_hotkey, self._handle_swap)
            self._registered_hotkeys.append(new_hotkey)
            self.swap_hotkey = new_hotkey
            return True
        except Exception as e:
            print(f"Chyba při změně swap zkratky: {e}")
            return False

    def unregister_all(self):
        """Odregistruje všechny klávesové zkratky"""
        keyboard.unhook_all()
        self._registered_hotkeys.clear()
