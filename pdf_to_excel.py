#!/usr/bin/env python3
"""
PDF to Excel Converter
A comprehensive tool to convert PDF files to Excel format using multiple extraction methods.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import pdfplumber
import tabula
import camelot
from PyPDF2 import PdfReader
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFToExcelConverter:
    """Main class for converting PDF files to Excel format."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_text_with_pdfplumber(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text and tables using pdfplumber."""
        results = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_data = {
                        'page': page_num,
                        'text': page.extract_text() or '',
                        'tables': []
                    }
                    
                    # Extract tables from the page
                    tables = page.extract_tables()
                    for table_num, table in enumerate(tables, 1):
                        if table and any(any(cell for cell in row) for row in table):
                            df = pd.DataFrame(table[1:], columns=table[0])
                            page_data['tables'].append({
                                'table_number': table_num,
                                'dataframe': df
                            })
                    
                    results.append(page_data)
                    
        except Exception as e:
            logger.error(f"Error extracting with pdfplumber: {e}")
            
        return results
    
    def extract_tables_with_tabula(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extract tables using tabula-py."""
        try:
            tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            return [df for df in tables if not df.empty]
        except Exception as e:
            logger.error(f"Error extracting with tabula: {e}")
            return []
    
    def extract_tables_with_camelot(self, pdf_path: str) -> List[pd.DataFrame]:
        """Extract tables using camelot-py."""
        try:
            tables = camelot.read_pdf(pdf_path, pages='all')
            return [table.df for table in tables if not table.df.empty]
        except Exception as e:
            logger.error(f"Error extracting with camelot: {e}")
            return []
    
    def create_excel_workbook(self, data: List[Dict[str, Any]], 
                             tabula_tables: List[pd.DataFrame],
                             camelot_tables: List[pd.DataFrame],
                             output_filename: str) -> str:
        """Create Excel workbook with extracted data."""
        
        wb = openpyxl.Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        # Add text content sheet
        if any(page['text'].strip() for page in data):
            ws_text = wb.create_sheet("Text Content")
            ws_text.append(["Page", "Text Content"])
            
            for page in data:
                if page['text'].strip():
                    ws_text.append([f"Page {page['page']}", page['text']])
            
            # Auto-adjust column widths
            for column in ws_text.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 100)
                ws_text.column_dimensions[column_letter].width = adjusted_width
        
        # Add pdfplumber tables
        table_count = 0
        for page in data:
            for table_info in page['tables']:
                table_count += 1
                sheet_name = f"Table_{table_count}_Page_{page['page']}"
                if len(sheet_name) > 31:  # Excel sheet name limit
                    sheet_name = f"T{table_count}_P{page['page']}"
                
                ws = wb.create_sheet(sheet_name)
                df = table_info['dataframe']
                
                # Write dataframe to worksheet
                for r in dataframe_to_rows(df, index=False, header=True):
                    ws.append(r)
                
                # Auto-adjust column widths
                for column in ws.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    ws.column_dimensions[column_letter].width = adjusted_width
        
        # Add tabula tables
        for i, df in enumerate(tabula_tables, 1):
            sheet_name = f"Tabula_Table_{i}"
            if len(sheet_name) > 31:
                sheet_name = f"Tabula_{i}"
            
            ws = wb.create_sheet(sheet_name)
            
            # Write dataframe to worksheet
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
        
        # Add camelot tables
        for i, df in enumerate(camelot_tables, 1):
            sheet_name = f"Camelot_Table_{i}"
            if len(sheet_name) > 31:
                sheet_name = f"Camelot_{i}"
            
            ws = wb.create_sheet(sheet_name)
            
            # Write dataframe to worksheet
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
        
        # Save workbook
        output_path = self.output_dir / output_filename
        wb.save(output_path)
        return str(output_path)
    
    def convert_pdf_to_excel(self, pdf_path: str, output_filename: Optional[str] = None) -> str:
        """Main conversion method."""
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if output_filename is None:
            pdf_name = Path(pdf_path).stem
            output_filename = f"{pdf_name}_converted.xlsx"
        
        logger.info(f"Converting {pdf_path} to Excel...")
        
        # Extract data using different methods
        logger.info("Extracting data with pdfplumber...")
        pdfplumber_data = self.extract_text_with_pdfplumber(pdf_path)
        
        logger.info("Extracting tables with tabula...")
        tabula_tables = self.extract_tables_with_tabula(pdf_path)
        
        logger.info("Extracting tables with camelot...")
        camelot_tables = self.extract_tables_with_camelot(pdf_path)
        
        # Create Excel workbook
        logger.info("Creating Excel workbook...")
        output_path = self.create_excel_workbook(
            pdfplumber_data, tabula_tables, camelot_tables, output_filename
        )
        
        logger.info(f"Conversion completed! Output saved to: {output_path}")
        return output_path

def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="Convert PDF files to Excel format")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output Excel filename")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    
    args = parser.parse_args()
    
    try:
        converter = PDFToExcelConverter(args.output_dir)
        output_path = converter.convert_pdf_to_excel(args.pdf_path, args.output)
        print(f"✅ Successfully converted PDF to Excel: {output_path}")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()