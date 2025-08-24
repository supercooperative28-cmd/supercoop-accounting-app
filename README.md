# PDF to Excel Converter

A powerful and comprehensive tool for converting PDF files to Excel format with multiple extraction methods for optimal accuracy.

## ✨ Features

- **Multiple Extraction Methods**: Uses pdfplumber, tabula-py, camelot-py, and PyPDF2 for comprehensive data extraction
- **Text & Table Extraction**: Extracts both text content and structured tables from PDFs
- **Organized Output**: Creates Excel workbooks with multiple sheets for different extraction methods
- **Command Line Interface**: Simple CLI for batch processing and automation
- **Web Interface**: Modern, responsive web application for easy file upload and conversion
- **Formatting**: Automatically formats Excel output with proper styling and column widths
- **Large File Support**: Handles PDFs up to 50MB

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd pdf-to-excel-converter

# Install dependencies
pip install -r requirements.txt
```

### 2. Command Line Usage

```bash
# Basic conversion
python pdf_to_excel.py document.pdf

# Specify output filename
python pdf_to_excel.py document.pdf -o converted_document.xlsx

# Specify output directory
python pdf_to_excel.py document.pdf -d my_output_folder
```

### 3. Web Interface

```bash
# Start the web server
python web_app.py

# Open your browser and go to: http://localhost:5000
```

## 📋 Requirements

- Python 3.7+
- Java Runtime Environment (JRE) for tabula-py
- OpenCV dependencies for camelot-py

### System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    default-jre \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1
```

#### CentOS/RHEL:
```bash
sudo yum install -y \
    java-1.8.0-openjdk \
    mesa-libGL \
    glib2 \
    libSM \
    libXext \
    libXrender
```

#### macOS:
```bash
brew install opencv
```

## 🔧 Usage Examples

### Command Line Examples

```bash
# Convert a single PDF
python pdf_to_excel.py report.pdf

# Convert with custom output name
python pdf_to_excel.py report.pdf -o financial_report.xlsx

# Convert to specific directory
python pdf_to_excel.py report.pdf -d /path/to/output

# Batch conversion (using shell)
for pdf in *.pdf; do
    python pdf_to_excel.py "$pdf"
done
```

### Python API Usage

```python
from pdf_to_excel import PDFToExcelConverter

# Create converter instance
converter = PDFToExcelConverter(output_dir="output")

# Convert PDF to Excel
output_path = converter.convert_pdf_to_excel("document.pdf", "output.xlsx")
print(f"Converted to: {output_path}")
```

## 📊 Output Structure

The generated Excel file contains multiple sheets:

1. **PDFPlumber_Extraction**: Text and tables extracted using pdfplumber
2. **Tabula_Tables**: Tables extracted using tabula-py
3. **Camelot_Tables**: Tables extracted using camelot-py
4. **PyPDF2_Text**: Text extracted using PyPDF2

Each sheet is organized with:
- Page headers for multi-page documents
- Structured table data
- Formatted text content
- Auto-adjusted column widths

## 🛠️ Configuration

### Web Application Settings

Edit `web_app.py` to customize:

```python
# File size limit (default: 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Upload folder
UPLOAD_FOLDER = 'uploads'

# Output folder
OUTPUT_FOLDER = 'output'

# Secret key (change in production)
app.secret_key = 'your-secret-key-here'
```

### Command Line Options

```bash
python pdf_to_excel.py --help

# Available options:
#   pdf_file          Path to the PDF file to convert
#   -o, --output     Output Excel filename (optional)
#   -d, --output-dir Output directory (default: output)
```

## 🔍 Troubleshooting

### Common Issues

1. **Java not found**: Install JRE for tabula-py functionality
2. **OpenCV errors**: Install system dependencies for camelot-py
3. **Memory issues**: Reduce file size or process in smaller chunks
4. **Permission errors**: Ensure write access to output directory

### Debug Mode

```bash
# Enable debug logging
export PYTHONPATH=.
python -u pdf_to_excel.py document.pdf 2>&1 | tee conversion.log
```

### Web App Debug

```bash
# Start with debug mode
FLASK_ENV=development python web_app.py
```

## 📁 Project Structure

```
pdf-to-excel-converter/
├── pdf_to_excel.py      # Main conversion script
├── web_app.py           # Flask web application
├── templates/
│   └── index.html      # Web interface template
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── uploads/            # Temporary upload directory
└── output/             # Generated Excel files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF text and table extraction
- [tabula-py](https://github.com/chezou/tabula-py) - Table extraction from PDFs
- [camelot-py](https://github.com/camelot-dev/camelot) - Advanced table extraction
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - PDF text extraction
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel file creation and manipulation

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the error logs
3. Open an issue on GitHub
4. Check the documentation for your specific use case

---

**Note**: This tool works best with PDFs that contain structured data, tables, or clear text. Scanned documents may require OCR preprocessing for optimal results.