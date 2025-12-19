#!/bin/bash
# Bionic Reading EPUB Converter - Linux Launcher
# Make executable: chmod +x run_bionic_reader.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 bionic_reader.py --gui

if [ $? -ne 0 ]; then
    echo ""
    echo "If you see errors, make sure you have:"
    echo "  1. Python 3 installed"
    echo "  2. Dependencies: pip install -r requirements.txt"
    echo "  3. tkinter: sudo dnf install python3-tkinter  (Nobara/Fedora)"
    echo "              sudo apt install python3-tk       (Ubuntu/Debian)"
    echo ""
    read -p "Press Enter to close..."
fi
