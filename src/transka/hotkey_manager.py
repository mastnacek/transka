# -*- coding: utf-8 -*-
"""
Hotkey Manager pro aplikaci Transka
Spravuje globální klávesové zkratky
"""
import keyboard
from typing import Callable


class HotkeyManager:
    """Správce globálních klávesových zkratek"""

    def __init__(
        self,
        main_hotkey: str,
        swap_hotkey: str,
        clear_hotkey: str,
        workflow_callback: Callable[[], None],
        swap_callback: Callable[[], None],
        clear_callback: Callable[[], None]
    ):
        """
        Inicializuje HotkeyManager

        Args:
            main_hotkey: Hlavní zkratka (např. "ctrl+alt+t")
            swap_hotkey: Zkratka pro swap jazyků (např. "ctrl+alt+s")
            clear_hotkey: Zkratka pro vymazání input pole (např. "ctrl+alt+c")
            workflow_callback: Callback funkce pro zpracování workflow hotkey
            swap_callback: Callback funkce pro swap jazyků
            clear_callback: Callback funkce pro vymazání input pole
        """
        self.main_hotkey = main_hotkey
        self.swap_hotkey = swap_hotkey
        self.clear_hotkey = clear_hotkey
        self.workflow_callback = workflow_callback
        self.swap_callback = swap_callback
        self.clear_callback = clear_callback
        self._registered_hotkeys = []

    def register_hotkeys(self):
        """Zaregistruje všechny globální klávesové zkratky"""
        try:
            # Hlavní zkratka (Ctrl+Alt+T)
            keyboard.add_hotkey(self.main_hotkey, self.workflow_callback)
            self._registered_hotkeys.append(self.main_hotkey)

            # Swap jazyků zkratka (Ctrl+Alt+S)
            keyboard.add_hotkey(self.swap_hotkey, self.swap_callback)
            self._registered_hotkeys.append(self.swap_hotkey)

            # Clear input pole zkratka (Ctrl+Alt+C)
            keyboard.add_hotkey(self.clear_hotkey, self.clear_callback)
            self._registered_hotkeys.append(self.clear_hotkey)

        except Exception as e:
            print(f"Chyba při nastavování zkratek: {e}")

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

            # Přidat novou zkratku
            keyboard.add_hotkey(new_hotkey, self.workflow_callback)
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
            new_hotkey: Nová zkratka (např. "ctrl+alt+d")

        Returns:
            bool: True pokud úspěšné, False při chybě
        """
        try:
            # Odstranit starou zkratku
            if self.swap_hotkey in self._registered_hotkeys:
                keyboard.remove_hotkey(self.swap_hotkey)
                self._registered_hotkeys.remove(self.swap_hotkey)

            # Přidat novou zkratku
            keyboard.add_hotkey(new_hotkey, self.swap_callback)
            self._registered_hotkeys.append(new_hotkey)
            self.swap_hotkey = new_hotkey
            return True
        except Exception as e:
            print(f"Chyba při změně swap zkratky: {e}")
            return False

    def update_clear_hotkey(self, new_hotkey: str):
        """
        Aktualizuje clear zkratku (pro live reload z Settings)

        Args:
            new_hotkey: Nová zkratka (např. "ctrl+alt+x")

        Returns:
            bool: True pokud úspěšné, False při chybě
        """
        try:
            # Odstranit starou zkratku
            if self.clear_hotkey in self._registered_hotkeys:
                keyboard.remove_hotkey(self.clear_hotkey)
                self._registered_hotkeys.remove(self.clear_hotkey)

            # Přidat novou zkratku
            keyboard.add_hotkey(new_hotkey, self.clear_callback)
            self._registered_hotkeys.append(new_hotkey)
            self.clear_hotkey = new_hotkey
            return True
        except Exception as e:
            print(f"Chyba při změně clear zkratky: {e}")
            return False

    def unregister_all(self):
        """Odregistruje všechny klávesové zkratky"""
        keyboard.unhook_all()
        self._registered_hotkeys.clear()
