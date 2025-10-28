@echo off
REM Spusteni DeepL Translator bez zobrazeného terminálu

REM Spuštění Pythonu přes uv s windoww režimem (bez konzole)
start "" /B uv run pythonw -m src.main

exit
