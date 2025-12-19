#!/usr/bin/env python3
"""
Bionic Reading EPUB Converter
Converts EPUB files to Bionic Reading format with bold word beginnings.
Cross-platform GUI application (Windows/Linux)
"""

import os
import sys
import regex
import zipfile
import threading
from pathlib import Path
from bs4 import BeautifulSoup

# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class BionicConverter:
    """Core conversion logic for Bionic Reading format."""
    
    SKIP_TAGS = {'script', 'style', 'pre', 'code', 'svg', 'math'}
    HTML_EXTENSIONS = ('.html', '.xhtml', '.htm')
    
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.word_pattern = regex.compile(r'\b[\p{L}\p{M}]+\b', regex.UNICODE)
    
    def bionic_word(self, word: str) -> str:
        """Convert a word to bionic format with bold beginning."""
        length = len(word)
        if length <= 1:
            return word
        elif length <= 3:
            bold_len = 1
        elif length <= 6:
            bold_len = 2
        elif length <= 9:
            bold_len = 3
        else:
            bold_len = length // 2
        
        return f"<b>{word[:bold_len]}</b>{word[bold_len:]}"
    
    def process_text(self, text: str) -> str:
        """Process text and apply bionic formatting to words."""
        if not text or not text.strip():
            return text
        return self.word_pattern.sub(lambda m: self.bionic_word(m.group(0)), text)
    
    def process_html_content(self, content: bytes) -> bytes:
        """Process HTML/XHTML content and apply bionic formatting."""
        try:
            # Try parsing as XML first (better for XHTML)
            soup = BeautifulSoup(content, 'xml')
        except Exception:
            # Fall back to lxml HTML parser
            soup = BeautifulSoup(content, 'lxml')
        
        # Find all text nodes and process them
        for element in soup.find_all(string=True):
            if element.parent and element.parent.name not in self.SKIP_TAGS:
                original = str(element)
                if original.strip():
                    new_text = self.process_text(original)
                    if new_text != original:
                        new_element = BeautifulSoup(new_text, 'html.parser')
                        element.replace_with(new_element)
        
        return str(soup).encode('utf-8')
    
    def convert_epub(self, input_path: str, output_path: str) -> tuple[bool, str]:
        """
        Convert an EPUB file to Bionic Reading format.
        Returns (success: bool, message: str)
        """
        try:
            if not os.path.exists(input_path):
                return False, f"Input file not found: {input_path}"
            
            with zipfile.ZipFile(input_path, 'r') as zip_in:
                file_list = zip_in.infolist()
                total_files = len(file_list)
                
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                    for i, file_info in enumerate(file_list):
                        with zip_in.open(file_info) as file:
                            content = file.read()
                            
                            # Process HTML/XHTML files
                            if file_info.filename.lower().endswith(self.HTML_EXTENSIONS):
                                content = self.process_html_content(content)
                            
                            zip_out.writestr(file_info, content)
                        
                        # Update progress
                        if self.progress_callback:
                            progress = int((i + 1) / total_files * 100)
                            self.progress_callback(progress, file_info.filename)
            
            return True, f"Successfully converted to: {output_path}"
            
        except zipfile.BadZipFile:
            return False, "Invalid EPUB file (not a valid ZIP archive)"
        except PermissionError:
            return False, "Permission denied. Check file permissions."
        except Exception as e:
            return False, f"Error during conversion: {str(e)}"


class BionicReaderGUI:
    """Cross-platform GUI for Bionic Reading converter."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bionic Reading EPUB Converter")
        self.root.geometry("600x400")
        self.root.minsize(500, 350)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.is_converting = False
        
        self._setup_ui()
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="📚 Bionic Reading Converter",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Input file section
        input_frame = ttk.LabelFrame(main_frame, text="Input EPUB", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        input_btn = ttk.Button(input_frame, text="Browse...", command=self._browse_input)
        input_btn.pack(side=tk.RIGHT)
        
        # Output file section
        output_frame = ttk.LabelFrame(main_frame, text="Output EPUB", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        output_btn = ttk.Button(output_frame, text="Browse...", command=self._browse_output)
        output_btn.pack(side=tk.RIGHT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="")
        self.progress_label.pack()
        
        # Convert button
        self.convert_btn = ttk.Button(
            main_frame,
            text="Convert to Bionic Reading",
            command=self._start_conversion,
            style='Accent.TButton'
        )
        self.convert_btn.pack(pady=20)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = ttk.Label(status_frame, textvariable=self.status_text)
        status_label.pack(side=tk.LEFT)
        
        # Configure style for button
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 11))
    
    def _browse_input(self):
        """Open file dialog for input EPUB."""
        filename = filedialog.askopenfilename(
            title="Select EPUB file",
            filetypes=[
                ("EPUB files", "*.epub"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            # Auto-generate output filename
            path = Path(filename)
            output_name = f"{path.stem}_bionic{path.suffix}"
            self.output_path.set(str(path.parent / output_name))
    
    def _browse_output(self):
        """Open file dialog for output EPUB."""
        filename = filedialog.asksaveasfilename(
            title="Save converted EPUB as",
            defaultextension=".epub",
            filetypes=[
                ("EPUB files", "*.epub"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_path.set(filename)
    
    def _update_progress(self, progress: int, current_file: str):
        """Update progress bar (called from conversion thread)."""
        self.root.after(0, lambda: self._do_update_progress(progress, current_file))
    
    def _do_update_progress(self, progress: int, current_file: str):
        """Actually update the UI (must be called from main thread)."""
        self.progress_bar['value'] = progress
        # Truncate long filenames
        if len(current_file) > 50:
            current_file = "..." + current_file[-47:]
        self.progress_label.config(text=f"{progress}% - {current_file}")
    
    def _start_conversion(self):
        """Start the conversion process in a background thread."""
        input_file = self.input_path.get().strip()
        output_file = self.output_path.get().strip()
        
        # Validation
        if not input_file:
            messagebox.showerror("Error", "Please select an input EPUB file.")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output file path.")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file not found:\n{input_file}")
            return
        
        if os.path.exists(output_file):
            if not messagebox.askyesno("Confirm", f"Output file exists. Overwrite?\n{output_file}"):
                return
        
        # Disable button during conversion
        self.convert_btn.config(state='disabled')
        self.is_converting = True
        self.status_text.set("Converting...")
        self.progress_bar['value'] = 0
        
        # Run conversion in background thread
        thread = threading.Thread(
            target=self._do_conversion,
            args=(input_file, output_file),
            daemon=True
        )
        thread.start()
    
    def _do_conversion(self, input_file: str, output_file: str):
        """Perform conversion (runs in background thread)."""
        converter = BionicConverter(progress_callback=self._update_progress)
        success, message = converter.convert_epub(input_file, output_file)
        
        # Update UI from main thread
        self.root.after(0, lambda: self._conversion_complete(success, message))
    
    def _conversion_complete(self, success: bool, message: str):
        """Handle conversion completion (called from main thread)."""
        self.is_converting = False
        self.convert_btn.config(state='normal')
        
        if success:
            self.status_text.set("Conversion complete!")
            self.progress_label.config(text="Done!")
            messagebox.showinfo("Success", message)
        else:
            self.status_text.set("Conversion failed")
            self.progress_label.config(text="")
            messagebox.showerror("Error", message)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main_cli():
    """Command-line interface for the converter."""
    import argparse
    from tqdm import tqdm
    
    parser = argparse.ArgumentParser(
        description='Convert EPUB to Bionic Reading format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.epub output.epub
  %(prog)s --gui
        """
    )
    parser.add_argument('input', nargs='?', help='Input EPUB file path')
    parser.add_argument('output', nargs='?', help='Output EPUB file path')
    parser.add_argument('--gui', '-g', action='store_true', help='Launch GUI mode')
    
    args = parser.parse_args()
    
    # Launch GUI if requested or if no arguments provided
    if args.gui or (args.input is None and args.output is None):
        app = BionicReaderGUI()
        app.run()
        return
    
    # CLI mode
    if not args.input or not args.output:
        parser.error("Both input and output paths are required for CLI mode")
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    if os.path.exists(args.output):
        print(f"Warning: Output file '{args.output}' will be overwritten.")
    
    # Progress bar for CLI
    pbar = None
    def progress_callback(progress, filename):
        nonlocal pbar
        if pbar is None:
            pbar = tqdm(total=100, desc="Converting", unit="%")
        pbar.n = progress
        pbar.set_postfix(file=filename[-30:] if len(filename) > 30 else filename)
        pbar.refresh()
    
    converter = BionicConverter(progress_callback=progress_callback)
    success, message = converter.convert_epub(args.input, args.output)
    
    if pbar:
        pbar.close()
    
    print(message)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main_cli()
