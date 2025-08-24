# 🚀 Quick Start Guide

## Install & Run in 3 Steps

### 1. Install Dependencies
```bash
# Option A: Use the installation script (recommended)
./install.sh

# Option B: Manual installation
pip install -r requirements.txt
```

### 2. Test the Installation
```bash
python3 test_converter.py
```

### 3. Start Converting!

#### Command Line (Single File)
```bash
python3 pdf_to_excel.py your_document.pdf
```

#### Web Interface (Easy Upload)
```bash
python3 web_app.py
# Open http://localhost:5000 in your browser
```

#### Batch Conversion (Multiple Files)
```bash
python3 batch_convert.py /path/to/pdfs
```

## 🎯 What You Get

- **Multiple Extraction Methods**: Uses 4 different PDF parsing libraries for best results
- **Organized Excel Output**: Separate sheets for text, tables, and different extraction methods
- **Professional Formatting**: Auto-sized columns, headers, and styling
- **Batch Processing**: Convert hundreds of PDFs at once
- **Web Interface**: Drag & drop PDF conversion

## 📁 Output Structure

Your Excel file will contain:
- **PDFPlumber_Extraction**: Main text and table content
- **Tabula_Tables**: Tables extracted with tabula-py
- **Camelot_Tables**: Advanced table extraction
- **PyPDF2_Text**: Additional text extraction

## 🔧 Troubleshooting

### Common Issues
- **Java not found**: Install JRE for tabula functionality
- **OpenCV errors**: Install system dependencies (see README.md)
- **Permission errors**: Ensure write access to output directory

### Get Help
```bash
# Run tests
python3 test_converter.py

# Try demo
python3 demo.py

# Check help
python3 pdf_to_excel.py --help
python3 batch_convert.py --help
```

## 💡 Pro Tips

1. **Best Results**: Use PDFs with clear text (not scanned images)
2. **Large Files**: Process files under 50MB for optimal performance
3. **Batch Mode**: Use `-w 8` for 8 parallel workers on powerful machines
4. **Custom Output**: Use `-o filename.xlsx` for custom Excel names

---

**Need more details?** See the full [README.md](README.md) for comprehensive documentation.