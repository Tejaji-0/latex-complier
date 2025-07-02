# LaTeX Compiler with Preview

A desktop application built with Python and Tkinter that provides a simple interface for writing, compiling, and previewing LaTeX documents in real-time.

## Features

- **Live LaTeX Editor**: Write LaTeX code in a convenient text editor with scroll support
- **One-click Compilation**: Compile LaTeX documents with a single button click
- **Real-time Preview**: View compiled PDF output directly in the application
- **PDF Export**: Save compiled documents to any location on your system
- **Error Handling**: Clear feedback when compilation fails
- **Clean Output Management**: Organized file structure with dedicated output directory

## Prerequisites

Before running the application, ensure you have the following installed:

### Required Software

- **Python 3.6+**
- **MiKTeX** (LaTeX distribution for Windows)
  - Download from: <https://miktex.org/download>
  - Make sure `pdflatex.exe` is accessible in your system

### Required Python Packages

```bash
pip install tkinter pillow PyMuPDF
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/latex-complier.git
cd latex-complier
```

2. Install required dependencies:

```bash
pip install pillow PyMuPDF
```

3. Ensure MiKTeX is installed and `pdflatex.exe` is available in your system PATH, or update the path in `main.py` to point to your MiKTeX installation.

## Usage

1. Run the application:

```bash
python main.py
```

2. **Write LaTeX Code**: Enter your LaTeX document in the text area. Here's a sample to get started:

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\title{My First Document}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This is a sample LaTeX document.

\section{Content}
You can write your content here with \textbf{bold text}, \textit{italic text}, and even mathematical equations like $E=mc^2$.

\end{document}
```

3. **Compile & Preview**: Click the "Compile & Preview" button to compile your LaTeX code and see the PDF preview
4. **Save PDF**: Use the "Save PDF" button to export your compiled document

## Project Structure

```text
latex-complier/
├── main.py              # Main application file
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── output/              # Generated files directory
    ├── document.tex     # Generated LaTeX file
    ├── document.pdf     # Compiled PDF output
    ├── document.aux     # LaTeX auxiliary files
    └── document.log     # Compilation log
```

## Configuration

### Customizing MiKTeX Path

If MiKTeX is installed in a different location, update the path in `main.py`:

```python
# Line 42 in main.py - update this path to your MiKTeX installation
subprocess.run(
    [r'C:\Users\psmsw\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe', 
     '-interaction=nonstopmode', f"{self.filename}.tex"],
    # ... rest of the configuration
)
```

### Changing Output Directory

You can modify the output directory by changing the `output_dir` variable in the `__init__` method:

```python
self.output_dir = "your_custom_output_directory"
```

## Troubleshooting

### Common Issues

1. **"Compilation failed" Error**
   - Check that your LaTeX syntax is correct
   - Ensure MiKTeX is properly installed
   - Verify the path to `pdflatex.exe` in the code

2. **"No PDF" Warning**
   - Make sure to compile your document first before trying to save
   - Check that the compilation was successful

3. **Preview Not Showing**
   - Ensure PyMuPDF is installed correctly
   - Check that the PDF was generated successfully in the output directory

4. **MiKTeX Not Found**
   - Install MiKTeX from <https://miktex.org/download>
   - Add MiKTeX to your system PATH, or update the executable path in the code

## Dependencies

- **tkinter**: GUI framework (included with Python)
- **PIL (Pillow)**: Image processing for PDF preview
- **PyMuPDF (fitz)**: PDF handling and rendering
- **subprocess**: System process management (included with Python)
- **os**: File system operations (included with Python)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Syntax highlighting for LaTeX code
- [ ] Multiple document tabs
- [ ] Template library
- [ ] Export to different formats
- [ ] Integrated spell checking
- [ ] LaTeX package manager integration
- [ ] Dark mode theme
- [ ] Zoom controls for preview

## Screenshots

Add screenshots of your application here

## Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

---

**Note**: This application is designed for Windows and requires MiKTeX. For other operating systems, you may need to modify the LaTeX compiler path and installation instructions.