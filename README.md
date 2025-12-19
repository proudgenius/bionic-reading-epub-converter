# Bionic Reading EPUB Converter

A cross-platform tool to convert EPUB files to Bionic Reading format, which bolds the beginning of words to help guide your eyes through text faster.

<img width="596" height="430" alt="image" src="https://github.com/user-attachments/assets/ab57aa48-a0fd-4a6d-ba27-fa77021590b7" />


## Features

- 📚 Convert any EPUB to Bionic Reading format
- 🖥️ Simple GUI (works on Windows & Linux)
- 💻 Command-line interface for scripting/automation
- 📊 Progress tracking
- 🔒 Preserves EPUB structure and metadata

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install tkinter (if not already installed)

**Windows:** Included with Python by default.

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora/Nobara:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

## Usage

### GUI Mode (Recommended)

Simply run the script without arguments or with `--gui`:

```bash
python bionic_reader.py
```

or

```bash
python bionic_reader.py --gui
```

Then:
1. Click "Browse..." to select your input EPUB
2. The output path is auto-generated (or choose your own)
3. Click "Convert to Bionic Reading"
4. Wait for completion!

### Command-Line Mode

```bash
python bionic_reader.py input.epub output.epub
```

**Examples:**
```bash
# Convert a book
python bionic_reader.py "My Book.epub" "My Book_bionic.epub"

# Force GUI mode
python bionic_reader.py --gui
```

## How It Works

Bionic Reading works by bolding the first part of each word, creating artificial fixation points that guide your eyes through text more efficiently:

**Regular text:**
> The quick brown fox jumps over the lazy dog.

**Bionic Reading:**
> **Th**e **qui**ck **bro**wn **fo**x **jum**ps **ov**er **th**e **la**zy **do**g.

The number of bolded characters scales with word length:
- 1-3 letters: 1 character bolded
- 4-6 letters: 2 characters bolded
- 7-9 letters: 3 characters bolded
- 10+ letters: half the word bolded

## Troubleshooting

### "No module named 'regex'"
```bash
pip install regex
```

### "No module named 'tkinter'"
See installation instructions above for your OS.

### EPUB not rendering correctly
Some e-readers may not fully support the bold formatting. Try a different reader app like Calibre, Kobo, or Apple Books.

## License

MIT License - Feel free to use and modify!
