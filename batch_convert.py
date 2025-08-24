#!/usr/bin/env python3
"""
Batch PDF to Excel Converter
Convert multiple PDF files to Excel format in batch mode.
"""

import os
import sys
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from pdf_to_excel import PDFToExcelConverter
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('batch_conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def convert_single_pdf(args):
    """Convert a single PDF file."""
    pdf_path, output_dir, converter = args
    
    try:
        logger.info(f"Converting: {pdf_path}")
        output_filename = f"{Path(pdf_path).stem}_converted.xlsx"
        output_path = converter.convert_pdf_to_excel(str(pdf_path), output_filename)
        logger.info(f"✅ Successfully converted: {pdf_path} -> {output_path}")
        return (pdf_path, True, output_path, None)
        
    except Exception as e:
        error_msg = f"Failed to convert {pdf_path}: {str(e)}"
        logger.error(error_msg)
        return (pdf_path, False, None, str(e))

def batch_convert(input_dir, output_dir, max_workers=4, file_pattern="*.pdf"):
    """Convert multiple PDF files in batch mode."""
    
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return False
    
    # Find all PDF files
    pdf_files = list(input_path.glob(file_pattern))
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir} matching pattern '{file_pattern}'")
        return False
    
    logger.info(f"Found {len(pdf_files)} PDF files to convert")
    
    # Create converter instance
    converter = PDFToExcelConverter(output_dir)
    
    # Prepare arguments for conversion
    conversion_args = [(pdf_file, output_dir, converter) for pdf_file in pdf_files]
    
    # Convert files using thread pool
    successful = 0
    failed = 0
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all conversion tasks
        future_to_pdf = {
            executor.submit(convert_single_pdf, args): args[0] 
            for args in conversion_args
        }
        
        # Process completed tasks
        for future in as_completed(future_to_pdf):
            pdf_path, success, output_path, error = future.result()
            results.append((pdf_path, success, output_path, error))
            
            if success:
                successful += 1
            else:
                failed += 1
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("BATCH CONVERSION SUMMARY")
    logger.info("="*60)
    logger.info(f"Total files processed: {len(pdf_files)}")
    logger.info(f"Successful conversions: {successful}")
    logger.info(f"Failed conversions: {failed}")
    logger.info(f"Success rate: {(successful/len(pdf_files)*100):.1f}%")
    
    if failed > 0:
        logger.info("\nFailed conversions:")
        for pdf_path, success, output_path, error in results:
            if not success:
                logger.info(f"  ❌ {pdf_path}: {error}")
    
    if successful > 0:
        logger.info(f"\nOutput directory: {output_dir}")
        logger.info("All converted Excel files are saved in the output directory.")
    
    return failed == 0

def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="Batch convert PDF files to Excel format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all PDFs in current directory
  python batch_convert.py .

  # Convert PDFs from specific directory
  python batch_convert.py /path/to/pdfs

  # Use custom output directory
  python batch_convert.py . -o /path/to/output

  # Use 8 parallel workers
  python batch_convert.py . -w 8

  # Convert only files matching pattern
  python batch_convert.py . -p "*report*.pdf"
        """
    )
    
    parser.add_argument(
        'input_dir',
        help='Input directory containing PDF files'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='output',
        help='Output directory for Excel files (default: output)'
    )
    
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=4,
        help='Maximum number of parallel workers (default: 4)'
    )
    
    parser.add_argument(
        '-p', '--pattern',
        default='*.pdf',
        help='File pattern to match (default: *.pdf)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be converted without actually converting'
    )
    
    args = parser.parse_args()
    
    # Validate input directory
    input_path = Path(args.input_dir)
    if not input_path.exists():
        logger.error(f"Input directory does not exist: {args.input_dir}")
        sys.exit(1)
    
    # Find PDF files
    pdf_files = list(input_path.glob(args.pattern))
    if not pdf_files:
        logger.error(f"No PDF files found in {args.input_dir} matching pattern '{args.pattern}'")
        sys.exit(1)
    
    logger.info(f"Found {len(pdf_files)} PDF files to convert:")
    for pdf_file in pdf_files:
        logger.info(f"  📄 {pdf_file}")
    
    if args.dry_run:
        logger.info("\nDry run mode - no files will be converted")
        sys.exit(0)
    
    # Create output directory
    output_path = Path(args.output_dir)
    output_path.mkdir(exist_ok=True)
    logger.info(f"Output directory: {output_path.absolute()}")
    
    # Start batch conversion
    logger.info(f"Starting batch conversion with {args.workers} workers...")
    
    try:
        success = batch_convert(
            args.input_dir,
            args.output_dir,
            args.workers,
            args.pattern
        )
        
        if success:
            logger.info("\n🎉 All conversions completed successfully!")
            sys.exit(0)
        else:
            logger.error("\n❌ Some conversions failed. Check the log above for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⚠️  Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n💥 Unexpected error during batch conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()