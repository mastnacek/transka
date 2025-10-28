# -*- coding: utf-8 -*-
"""
System Tray Manager pro aplikaci Transka
Spravuje system tray ikonu a menu
"""
import threading
from typing import Callable, Optional
import pystray
from PIL import Image, ImageDraw


class TrayManager:
    """Správce system tray ikony"""

    def __init__(
        self,
        app_name: str,
        on_show: Callable[[], None],
        on_settings: Callable[[], None],
        on_quit: Callable[[], None]
    ):
        """
        Inicializuje TrayManager

        Args:
            app_name: Název aplikace pro tooltip
            on_show: Callback pro zobrazení hlavního okna
            on_settings: Callback pro zobrazení nastavení
            on_quit: Callback pro ukončení aplikace
        """
        self.app_name = app_name
        self.on_show = on_show
        self.on_settings = on_settings
        self.on_quit = on_quit
        self.tray_icon: Optional[pystray.Icon] = None

    def _create_icon_image(self) -> Image.Image:
        """Vytvoří jednoduchou ikonu pro system tray"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(33, 150, 243))
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            [width // 4, height // 4, width * 3 // 4, height * 3 // 4],
            fill=(255, 255, 255)
        )
        return image

    def start(self):
        """Spustí system tray ikonu v separátním vlákně"""
        # Menu pro tray
        menu = pystray.Menu(
            pystray.MenuItem("Zobrazit", self.on_show),
            pystray.MenuItem("Nastavení", self.on_settings),
            pystray.MenuItem("Ukončit", self.on_quit)
        )

        self.tray_icon = pystray.Icon(
            self.app_name.lower(),
            self._create_icon_image(),
            self.app_name,
            menu
        )

        # Spuštění tray ikony v separátním vlákně
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()

    def stop(self):
        """Zastaví system tray ikonu"""
        if self.tray_icon:
            self.tray_icon.stop()
