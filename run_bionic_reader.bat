@echo off
REM Bionic Reading EPUB Converter - Windows Launcher
REM Double-click this file to launch the GUI

python "%~dp0bionic_reader.py" --gui
if errorlevel 1 (
    echo.
    echo If you see errors, make sure you have:
    echo   1. Python installed (python.org)
    echo   2. Dependencies installed: pip install -r requirements.txt
    echo.
    pause
)
