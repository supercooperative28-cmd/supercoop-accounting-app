# PDF to Excel Converter

A powerful Python tool to convert PDF files containing tables and structured data into Excel format (.xlsx). This converter can handle various types of PDF content including tables, text data, and mixed content across multiple pages.

## Features

- **Table Extraction**: Automatically detects and extracts tables from PDF files
- **Text Parsing**: Converts structured text data into tabular format
- **Multi-page Support**: Processes PDFs with multiple pages
- **Multiple Output Sheets**: Creates separate Excel sheets for different tables/data
- **Fallback Text Extraction**: Extracts all text when no tables are found
- **Command Line Interface**: Easy-to-use CLI with verbose logging
- **Error Handling**: Robust error handling with informative messages

## Installation

### Prerequisites

- Python 3.7 or higher
- Virtual environment (recommended)

### Setup

1. **Clone or download the repository:**
   ```bash
   git clone <repository-url>
   cd pdf-to-excel-converter
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv pdf_converter_env
   source pdf_converter_env/bin/activate  # On Windows: pdf_converter_env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Convert a PDF to Excel:
```bash
python pdf_to_excel_converter.py input.pdf output.xlsx
```

### Advanced Usage

With verbose logging:
```bash
python pdf_to_excel_converter.py input.pdf output.xlsx --verbose
```

With specific extraction method:
```bash
python pdf_to_excel_converter.py input.pdf output.xlsx --method pdfplumber
```

### Command Line Options

- `input_pdf`: Path to the input PDF file (required)
- `output_excel`: Path to the output Excel file (required)
- `--method`: Extraction method to use (default: pdfplumber)
- `--verbose`, `-v`: Enable verbose logging for debugging

## Examples

### Example 1: Converting a Sales Report

```bash
# Convert a sales report PDF to Excel
python pdf_to_excel_converter.py sales_report.pdf sales_data.xlsx

# With verbose output to see the process
python pdf_to_excel_converter.py sales_report.pdf sales_data.xlsx --verbose
```

### Example 2: Processing Employee Data

```bash
# Convert employee data PDF
python pdf_to_excel_converter.py employee_records.pdf employee_data.xlsx
```

### Example 3: Batch Processing (using shell script)

Create a batch processing script:
```bash
#!/bin/bash
for pdf_file in *.pdf; do
    excel_file="${pdf_file%.pdf}.xlsx"
    python pdf_to_excel_converter.py "$pdf_file" "$excel_file"
    echo "Converted $pdf_file to $excel_file"
done
```

## Testing

The repository includes a sample PDF generator and test files:

### Generate Sample PDF

```bash
python create_sample_pdf.py
```

This creates `sample_data.pdf` with tables containing:
- Sales data (Product, Units Sold, Revenue, Profit)
- Employee information (ID, Name, Department, Salary, Start Date)
- Summary information

### Test the Converter

```bash
python pdf_to_excel_converter.py sample_data.pdf sample_output.xlsx --verbose
```

## Output Format

The converter creates Excel files with the following structure:

- **Multiple Sheets**: Each table or data section becomes a separate sheet
- **Sheet Names**: Automatically named based on page and table number (e.g., "Page_1_Table_1")
- **Headers**: First row of tables becomes column headers
- **Fallback Sheet**: If no tables are found, creates a sheet with all extracted text

### Sample Output Structure

```
sample_output.xlsx
├── Page_1_Table_1 (Sales Data)
│   ├── Month | Product | Units Sold | Revenue | Profit
│   ├── January | Widget A | 150 | $15,000 | $4,500
│   └── ...
└── Page_1_Table_2 (Employee Data)
    ├── Employee ID | Name | Department | Salary | Start Date
    ├── EMP001 | John Smith | Engineering | $75,000 | 2020-01-15
    └── ...
```

## Supported PDF Types

- **Structured Tables**: PDFs with clear table formatting
- **Text-based Data**: Structured text that can be parsed into columns
- **Mixed Content**: PDFs with both tables and text
- **Multi-page Documents**: Documents spanning multiple pages

## Dependencies

The converter relies on these Python packages:

- **pandas**: Data manipulation and Excel writing
- **openpyxl**: Excel file format support  
- **pdfplumber**: PDF text and table extraction
- **pathlib2**: Enhanced path handling

## Troubleshooting

### Common Issues

1. **"No module named 'pdfplumber'"**
   - Solution: Ensure virtual environment is activated and dependencies are installed

2. **"No tables or structured data found"**
   - The PDF might contain images or unstructured text
   - Check the fallback text extraction sheet for raw content

3. **"Permission denied" errors**
   - Ensure you have write permissions to the output directory
   - Close the Excel file if it's already open

4. **Empty or corrupted output**
   - The PDF might be image-based or password protected
   - Try using different PDF files or OCR tools first

### Debug Mode

Use verbose mode to see detailed processing information:
```bash
python pdf_to_excel_converter.py input.pdf output.xlsx --verbose
```

This shows:
- Page-by-page processing
- Table detection results
- Row and column counts
- Error details

## Limitations

- **Image-based PDFs**: Cannot extract text from scanned documents (requires OCR)
- **Password-protected PDFs**: Must be unlocked before processing
- **Complex layouts**: Very complex table layouts might not be parsed correctly
- **Merged cells**: Complex cell merging might not be preserved

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with various PDF types
5. Submit a pull request

## License

This project is open source. Please check the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Run with `--verbose` flag for detailed logs
3. Create an issue with sample PDF (if possible)
4. Include error messages and system information

---

**Note**: This tool works best with PDFs that contain structured data. For image-based PDFs, consider using OCR tools first to convert them to text-based PDFs.