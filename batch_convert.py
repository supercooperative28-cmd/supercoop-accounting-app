#!/usr/bin/env python3
"""
Batch PDF to Excel converter.

This script processes all PDF files in a directory and converts them to Excel format.
Useful for processing multiple PDF files at once.
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from pdf_to_excel_converter import PDFToExcelConverter

def batch_convert(input_dir=".", output_dir=None, pattern="*.pdf", verbose=False):
    """
    Convert all PDF files in a directory to Excel format.
    
    Args:
        input_dir: Directory containing PDF files
        output_dir: Directory for output Excel files (default: same as input)
        pattern: File pattern to match (default: *.pdf)
        verbose: Enable verbose logging
    """
    
    if output_dir is None:
        output_dir = input_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    pdf_files = glob.glob(os.path.join(input_dir, pattern))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {input_dir} matching pattern '{pattern}'")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files to convert")
    print(f"📂 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir}")
    print("-" * 50)
    
    # Create converter
    converter = PDFToExcelConverter()
    
    # Track results
    successful = 0
    failed = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        # Create output filename
        pdf_name = Path(pdf_file).stem
        excel_file = os.path.join(output_dir, f"{pdf_name}.xlsx")
        
        print(f"[{i}/{len(pdf_files)}] Converting: {os.path.basename(pdf_file)}")
        
        try:
            # Convert PDF to Excel
            success = converter.convert_pdf_to_excel(pdf_file, excel_file)
            
            if success:
                successful += 1
                file_size = os.path.getsize(excel_file)
                print(f"   ✅ Success → {os.path.basename(excel_file)} ({file_size} bytes)")
            else:
                failed += 1
                print(f"   ❌ Failed → Conversion unsuccessful")
                
        except Exception as e:
            failed += 1
            print(f"   ❌ Error → {str(e)}")
            if verbose:
                import traceback
                print(f"   📋 Details: {traceback.format_exc()}")
    
    print("-" * 50)
    print(f"🎉 Batch conversion completed!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success rate: {successful/(successful+failed)*100:.1f}%" if (successful+failed) > 0 else "N/A")
    
    if successful > 0:
        print(f"📁 Excel files saved to: {output_dir}")

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description='Batch convert PDF files to Excel format')
    parser.add_argument('--input-dir', '-i', default='.', 
                       help='Input directory containing PDF files (default: current directory)')
    parser.add_argument('--output-dir', '-o', default=None,
                       help='Output directory for Excel files (default: same as input)')
    parser.add_argument('--pattern', '-p', default='*.pdf',
                       help='File pattern to match (default: *.pdf)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose error reporting')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"❌ Error: Input directory '{args.input_dir}' does not exist")
        sys.exit(1)
    
    # Run batch conversion
    batch_convert(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pattern=args.pattern,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()