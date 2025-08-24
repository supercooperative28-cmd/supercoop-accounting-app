#!/usr/bin/env python3
"""
Example usage of the PDF to Excel converter.

This script demonstrates how to use the PDFToExcelConverter class
programmatically rather than via the command line.
"""

import os
import sys
from pdf_to_excel_converter import PDFToExcelConverter

def main():
    """Example usage of the PDF to Excel converter."""
    
    # Create converter instance
    converter = PDFToExcelConverter()
    
    # Example 1: Basic conversion
    print("Example 1: Basic PDF to Excel conversion")
    print("-" * 40)
    
    input_pdf = "sample_data.pdf"
    output_excel = "example_output.xlsx"
    
    if os.path.exists(input_pdf):
        success = converter.convert_pdf_to_excel(input_pdf, output_excel)
        
        if success:
            print(f"✅ Successfully converted {input_pdf} to {output_excel}")
            print(f"📁 Output file size: {os.path.getsize(output_excel)} bytes")
        else:
            print(f"❌ Failed to convert {input_pdf}")
    else:
        print(f"❌ Input file {input_pdf} not found")
        print("💡 Run 'python create_sample_pdf.py' first to create a sample PDF")
    
    print()
    
    # Example 2: Extract and display table information
    print("Example 2: Extract table information")
    print("-" * 40)
    
    if os.path.exists(input_pdf):
        try:
            tables = converter.extract_tables_from_pdf(input_pdf)
            
            print(f"📊 Found {len(tables)} tables in the PDF:")
            
            for i, table in enumerate(tables, 1):
                table_name = getattr(table, 'name', f'Table_{i}')
                print(f"  Table {i}: {table_name}")
                print(f"    Rows: {len(table)}")
                print(f"    Columns: {len(table.columns)}")
                print(f"    Column names: {', '.join(table.columns[:5])}{'...' if len(table.columns) > 5 else ''}")
                print()
                
                # Show first few rows
                if len(table) > 0:
                    print("    Sample data:")
                    print(table.head(3).to_string(index=False))
                    print()
                    
        except Exception as e:
            print(f"❌ Error extracting tables: {str(e)}")
    
    # Example 3: Batch processing multiple PDFs
    print("Example 3: Batch processing (if multiple PDFs exist)")
    print("-" * 40)
    
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if len(pdf_files) > 1:
        print(f"Found {len(pdf_files)} PDF files:")
        
        for pdf_file in pdf_files:
            excel_file = pdf_file.replace('.pdf', '_converted.xlsx')
            print(f"  Converting {pdf_file} → {excel_file}")
            
            success = converter.convert_pdf_to_excel(pdf_file, excel_file)
            status = "✅" if success else "❌"
            print(f"    {status} {'Success' if success else 'Failed'}")
    else:
        print("Only one PDF file found. Create more PDFs for batch processing demonstration.")
    
    print()
    print("🎉 Example usage completed!")
    print()
    print("Next steps:")
    print("1. Try converting your own PDF files")
    print("2. Use the command line tool: python pdf_to_excel_converter.py input.pdf output.xlsx")
    print("3. Check the generated Excel files in your spreadsheet application")

if __name__ == "__main__":
    main()