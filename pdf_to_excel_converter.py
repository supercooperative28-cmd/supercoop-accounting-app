#!/usr/bin/env python3
"""
PDF to Excel Converter

This script converts PDF files to Excel format, handling different types of content:
- Tables in PDFs
- Text content organized into structured data
- Multiple pages

Dependencies:
- pandas: Data manipulation and Excel writing
- openpyxl: Excel file format support
- pdfplumber: PDF text and table extraction
- tabula-py: Alternative table extraction (requires Java)

Usage:
    python pdf_to_excel_converter.py input.pdf output.xlsx
"""

import sys
import pandas as pd
import pdfplumber
import argparse
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PDFToExcelConverter:
    """Convert PDF files to Excel format with table and text extraction."""
    
    def __init__(self):
        self.extracted_data = []
        
    def extract_tables_from_pdf(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extract tables from PDF using pdfplumber."""
        tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                logger.info(f"Processing PDF with {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.info(f"Processing page {page_num}")
                    
                    # Extract tables from the page
                    page_tables = page.extract_tables()
                    
                    if page_tables:
                        for table_num, table in enumerate(page_tables, 1):
                            if table and len(table) > 1:  # Ensure table has data
                                # Convert table to DataFrame
                                df = pd.DataFrame(table[1:], columns=table[0])
                                df.name = f"Page_{page_num}_Table_{table_num}"
                                tables.append(df)
                                logger.info(f"Extracted table with {len(df)} rows and {len(df.columns)} columns")
                    
                    # If no tables found, try to extract structured text
                    if not page_tables:
                        text_data = self.extract_text_as_table(page)
                        if text_data:
                            df = pd.DataFrame(text_data)
                            df.name = f"Page_{page_num}_Text"
                            tables.append(df)
                            
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            raise
            
        return tables
    
    def extract_text_as_table(self, page) -> Optional[List[Dict[str, Any]]]:
        """Extract text and try to structure it as tabular data."""
        text = page.extract_text()
        
        if not text:
            return None
            
        lines = text.strip().split('\n')
        
        # Try to detect structured data patterns
        structured_data = []
        
        # Look for key-value pairs or columnar data
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to split by common delimiters
            if '\t' in line:
                parts = line.split('\t')
            elif '|' in line:
                parts = line.split('|')
            elif ':' in line and len(line.split(':')) == 2:
                # Key-value pair
                key, value = line.split(':', 1)
                structured_data.append({'Key': key.strip(), 'Value': value.strip()})
                continue
            else:
                # Try to split by multiple spaces
                parts = re.split(r'\s{2,}', line)
            
            if len(parts) > 1:
                # Create a row with numbered columns
                row = {f'Column_{i+1}': part.strip() for i, part in enumerate(parts) if part.strip()}
                if row:
                    structured_data.append(row)
        
        return structured_data if structured_data else None
    
    def convert_pdf_to_excel(self, pdf_path: str, excel_path: str, method: str = 'pdfplumber') -> bool:
        """
        Convert PDF to Excel file.
        
        Args:
            pdf_path: Path to input PDF file
            excel_path: Path to output Excel file
            method: Extraction method ('pdfplumber' or 'tabula')
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Validate input file
            if not Path(pdf_path).exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return False
            
            # Extract tables based on method
            if method == 'pdfplumber':
                tables = self.extract_tables_from_pdf(pdf_path)
            else:
                logger.error(f"Unsupported method: {method}")
                return False
            
            if not tables:
                logger.warning("No tables or structured data found in PDF")
                # Create a simple text extraction as fallback
                tables = self.extract_all_text_fallback(pdf_path)
            
            # Write to Excel
            self.write_to_excel(tables, excel_path)
            logger.info(f"Successfully converted PDF to Excel: {excel_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error during conversion: {str(e)}")
            return False
    
    def extract_all_text_fallback(self, pdf_path: str) -> List[pd.DataFrame]:
        """Fallback method to extract all text when no tables are found."""
        all_text = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        for line_num, line in enumerate(lines, 1):
                            all_text.append({
                                'Page': page_num,
                                'Line': line_num,
                                'Content': line
                            })
        except Exception as e:
            logger.error(f"Error in fallback text extraction: {str(e)}")
        
        if all_text:
            df = pd.DataFrame(all_text)
            df.name = "All_Text_Content"
            return [df]
        
        return []
    
    def write_to_excel(self, tables: List[pd.DataFrame], excel_path: str):
        """Write extracted tables to Excel file with multiple sheets."""
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            if not tables:
                # Create empty sheet
                pd.DataFrame({'Message': ['No data extracted from PDF']}).to_excel(
                    writer, sheet_name='No_Data', index=False
                )
            else:
                for i, table in enumerate(tables):
                    # Clean sheet name (Excel has limitations)
                    sheet_name = getattr(table, 'name', f'Sheet_{i+1}')
                    sheet_name = re.sub(r'[^\w\s-]', '_', sheet_name)[:31]  # Excel limit is 31 chars
                    
                    # Write table to sheet
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
                    logger.info(f"Written sheet: {sheet_name} with {len(table)} rows")


def main():
    """Main function to handle command line arguments and run conversion."""
    parser = argparse.ArgumentParser(description='Convert PDF files to Excel format')
    parser.add_argument('input_pdf', help='Path to input PDF file')
    parser.add_argument('output_excel', help='Path to output Excel file')
    parser.add_argument('--method', choices=['pdfplumber'], default='pdfplumber',
                       help='Extraction method to use (default: pdfplumber)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create converter instance
    converter = PDFToExcelConverter()
    
    # Convert PDF to Excel
    success = converter.convert_pdf_to_excel(args.input_pdf, args.output_excel, args.method)
    
    if success:
        print(f"✅ Successfully converted {args.input_pdf} to {args.output_excel}")
        sys.exit(0)
    else:
        print(f"❌ Failed to convert {args.input_pdf}")
        sys.exit(1)


if __name__ == "__main__":
    main()