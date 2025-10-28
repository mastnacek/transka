# -*- coding: utf-8 -*-
"""
DeepL Translator - Desktop aplikace pro rychlý překlad
"""
__version__ = "1.0.0"

# Hlavní exports pro použití jako knihovna
from transka.deepl_translator import DeepLTranslator
from transka.google_translator import GoogleTranslator
from transka.base_translator import BaseTranslator, UsageInfo
from transka.config import Config

__all__ = [
    "DeepLTranslator",
    "GoogleTranslator",
    "BaseTranslator",
    "UsageInfo",
    "Config",
]
