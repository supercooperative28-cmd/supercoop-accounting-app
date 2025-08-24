# PDF to Excel Converter

A powerful and comprehensive tool for converting PDF files to Excel format with multiple extraction methods and a beautiful web interface.

## Features

- **Multiple Extraction Methods**: Uses pdfplumber, tabula-py, and camelot-py for robust table extraction
- **Text Extraction**: Extracts and organizes text content by page
- **Table Detection**: Automatically detects and extracts tables from PDFs
- **Excel Formatting**: Creates well-formatted Excel files with proper column widths
- **Web Interface**: Modern, responsive web application with drag-and-drop functionality
- **Command Line Tool**: CLI interface for batch processing and automation
- **Multiple Output Sheets**: Organizes data into separate sheets for better readability

## Installation

### Prerequisites

- Python 3.8 or higher
- Java Runtime Environment (JRE) for tabula-py
- Ghostscript for camelot-py

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y default-jre ghostscript

# Install system dependencies (CentOS/RHEL)
sudo yum install -y java-11-openjdk ghostscript

# Install system dependencies (macOS)
brew install openjdk ghostscript
```

## Usage

### Command Line Interface

```bash
# Basic conversion
python pdf_to_excel.py document.pdf

# Specify output filename
python pdf_to_excel.py document.pdf -o converted_document.xlsx

# Specify output directory
python pdf_to_excel.py document.pdf --output-dir /path/to/output
```

### Web Interface

1. Start the web application:
```bash
python web_app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Drag and drop a PDF file or click to browse

4. Click "Convert to Excel" and wait for processing

5. Download the converted Excel file

## How It Works

The converter uses multiple extraction methods to ensure the best possible results:

1. **pdfplumber**: Extracts text and simple tables with high accuracy
2. **tabula-py**: Specialized in table extraction from PDFs
3. **camelot-py**: Advanced table extraction with better handling of complex layouts

The extracted data is organized into Excel sheets:
- **Text Content**: All text content organized by page
- **Table sheets**: Each detected table gets its own sheet
- **Multiple extraction methods**: Results from different tools are preserved

## File Structure

```
├── pdf_to_excel.py      # Main conversion script
├── web_app.py           # Flask web application
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── requirements.txt     # Python dependencies
├── uploads/            # Temporary upload directory
├── output/             # Converted Excel files
└── README.md           # This file
```

## API Endpoints

- `GET /`: Main web interface
- `POST /upload`: File upload and conversion
- `GET /download/<filename>`: Download converted file
- `GET /health`: Health check endpoint

## Configuration

### Web App Settings

Edit `web_app.py` to customize:
- File size limits
- Upload directory
- Output directory
- Secret key (for production)

### Conversion Settings

Modify `pdf_to_excel.py` to adjust:
- Table detection parameters
- Text extraction options
- Excel formatting preferences

## Troubleshooting

### Common Issues

1. **Java not found**: Install JRE for tabula-py
2. **Ghostscript error**: Install Ghostscript for camelot-py
3. **Permission errors**: Ensure write access to output directories
4. **Memory issues**: Large PDFs may require more RAM

### Performance Tips

- Use smaller PDF files for faster processing
- Close other applications to free up memory
- Process files in batches for multiple conversions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on GitHub

## Changelog

### Version 1.0.0
- Initial release
- Multiple extraction methods
- Web interface
- Command line tool
- Excel formatting