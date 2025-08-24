#!/usr/bin/env python3
"""
Example usage of the PDF to Excel converter
Demonstrates how to use the converter in your own Python scripts.
"""

from pdf_to_excel import PDFToExcelConverter
import os

def main():
    """Example usage of the PDF to Excel converter."""
    
    # Initialize the converter
    converter = PDFToExcelConverter(output_dir="example_output")
    
    # Example 1: Basic conversion
    print("Example 1: Basic conversion")
    try:
        # Replace 'sample.pdf' with your actual PDF file path
        if os.path.exists("sample.pdf"):
            output_path = converter.convert_pdf_to_excel("sample.pdf")
            print(f"✅ Converted to: {output_path}")
        else:
            print("⚠️  sample.pdf not found. Please place a PDF file in the current directory.")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Custom output filename
    print("Example 2: Custom output filename")
    try:
        if os.path.exists("sample.pdf"):
            output_path = converter.convert_pdf_to_excel(
                "sample.pdf", 
                "my_custom_filename.xlsx"
            )
            print(f"✅ Converted to: {output_path}")
        else:
            print("⚠️  sample.pdf not found. Please place a PDF file in the current directory.")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Batch processing
    print("Example 3: Batch processing")
    pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]
    
    if pdf_files:
        print(f"Found {len(pdf_files)} PDF files:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file}")
        
        print("\nProcessing each file...")
        for pdf_file in pdf_files:
            try:
                output_path = converter.convert_pdf_to_excel(pdf_file)
                print(f"✅ {pdf_file} -> {output_path}")
            except Exception as e:
                print(f"❌ {pdf_file} failed: {e}")
    else:
        print("No PDF files found in current directory.")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Using different output directories
    print("Example 4: Using different output directories")
    
    # Create a converter with a specific output directory
    custom_converter = PDFToExcelConverter(output_dir="custom_output")
    
    try:
        if os.path.exists("sample.pdf"):
            output_path = custom_converter.convert_pdf_to_excel("sample.pdf")
            print(f"✅ Converted to: {output_path}")
        else:
            print("⚠️  sample.pdf not found. Please place a PDF file in the current directory.")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

def create_sample_pdf():
    """Create a sample PDF file for testing (if reportlab is available)."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a simple PDF with text and tables
        c = canvas.Canvas("sample.pdf", pagesize=letter)
        width, height = letter
        
        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Sample PDF Document")
        
        # Add some text
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 150, "This is a sample PDF file for testing the converter.")
        c.drawString(100, height - 170, "It contains text content and some structured data.")
        
        # Add a simple table-like structure
        y_position = height - 250
        c.drawString(100, y_position, "Name")
        c.drawString(200, y_position, "Age")
        c.drawString(300, y_position, "City")
        
        y_position -= 20
        c.drawString(100, y_position, "John Doe")
        c.drawString(200, y_position, "30")
        c.drawString(300, y_position, "New York")
        
        y_position -= 20
        c.drawString(100, y_position, "Jane Smith")
        c.drawString(200, y_position, "25")
        c.drawString(300, y_position, "Los Angeles")
        
        c.save()
        print("✅ Created sample.pdf for testing")
        return True
        
    except ImportError:
        print("⚠️  reportlab not available. Cannot create sample PDF.")
        print("   Install with: pip install reportlab")
        return False
    except Exception as e:
        print(f"❌ Error creating sample PDF: {e}")
        return False

if __name__ == "__main__":
    print("PDF to Excel Converter - Example Usage")
    print("=" * 50)
    
    # Try to create a sample PDF if none exists
    if not os.path.exists("sample.pdf"):
        print("No sample PDF found. Creating one for testing...")
        create_sample_pdf()
    
    print("\nRunning examples...\n")
    main()
    
    print("\n" + "="*50)
    print("Example usage completed!")
    print("\nTo run the web interface:")
    print("  python web_app.py")
    print("\nTo use the command line tool:")
    print("  python pdf_to_excel.py your_file.pdf")