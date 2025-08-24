#!/usr/bin/env python3
"""
PDF to Excel Converter Demo
This script demonstrates the various features of the converter.
"""

import os
import sys
from pathlib import Path

def create_sample_pdf():
    """Create a sample PDF for demonstration."""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        
        sample_pdf = "demo_sample.pdf"
        c = canvas.Canvas(sample_pdf, pagesize=letter)
        
        # Page 1: Title and introduction
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 750, "Sample Financial Report")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "This is a demonstration PDF for the PDF to Excel converter.")
        c.drawString(100, 700, "It contains various types of content including text and tables.")
        
        # Add a simple table
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 650, "Financial Summary Table:")
        
        # Table headers
        headers = ["Category", "Q1", "Q2", "Q3", "Q4", "Total"]
        x_positions = [100, 200, 250, 300, 350, 420]
        
        c.setFont("Helvetica-Bold", 10)
        for i, header in enumerate(headers):
            c.drawString(x_positions[i], 620, header)
        
        # Table data
        data = [
            ["Revenue", "1000", "1200", "1100", "1300", "4600"],
            ["Expenses", "800", "900", "850", "950", "3500"],
            ["Profit", "200", "300", "250", "350", "1100"]
        ]
        
        c.setFont("Helvetica", 10)
        y_start = 600
        for row_idx, row in enumerate(data):
            y_pos = y_start - (row_idx * 20)
            for col_idx, cell in enumerate(row):
                c.drawString(x_positions[col_idx], y_pos, cell)
        
        # Page 2: More content
        c.showPage()
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, "Page 2: Additional Information")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, "This page demonstrates multi-page PDF handling.")
        
        # Add some bullet points
        bullet_points = [
            "• Multiple extraction methods are used",
            "• Tables are automatically detected",
            "• Text formatting is preserved",
            "• Output is organized in Excel sheets"
        ]
        
        y_pos = 680
        for point in bullet_points:
            c.drawString(120, y_pos, point)
            y_pos -= 20
        
        c.save()
        print(f"✅ Sample PDF created: {sample_pdf}")
        return sample_pdf
        
    except ImportError:
        print("⚠️  reportlab not installed. Creating a simple text-based sample...")
        return create_simple_sample()
    except Exception as e:
        print(f"❌ Error creating sample PDF: {e}")
        return None

def create_simple_sample():
    """Create a simple text-based sample if reportlab is not available."""
    sample_pdf = "demo_sample.pdf"
    
    # This is a placeholder - in a real scenario, you'd need a PDF library
    print(f"📝 Please create a PDF file named '{sample_pdf}' manually for testing")
    print("   You can use any PDF document you have available.")
    return sample_pdf

def run_demo():
    """Run the main demo."""
    print("🚀 PDF to Excel Converter - Demo")
    print("=" * 50)
    
    # Check if converter is available
    try:
        from pdf_to_excel import PDFToExcelConverter
        print("✅ PDF to Excel converter imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import converter: {e}")
        print("Please install dependencies first: pip install -r requirements.txt")
        return False
    
    # Create sample PDF
    print("\n📄 Creating sample PDF for demonstration...")
    sample_pdf = create_sample_pdf()
    
    if not sample_pdf or not Path(sample_pdf).exists():
        print("⚠️  No sample PDF available. Demo cannot continue.")
        print("Please create a PDF file manually or install reportlab for automatic sample creation.")
        return False
    
    # Demonstrate conversion
    print(f"\n🔄 Converting sample PDF: {sample_pdf}")
    
    try:
        converter = PDFToExcelConverter("demo_output")
        output_path = converter.convert_pdf_to_excel(sample_pdf, "demo_output.xlsx")
        
        print(f"✅ Conversion successful!")
        print(f"📁 Output file: {output_path}")
        
        # Show file info
        if Path(output_path).exists():
            file_size = Path(output_path).stat().st_size
            print(f"📊 File size: {file_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def show_usage_examples():
    """Show usage examples."""
    print("\n📖 Usage Examples:")
    print("-" * 30)
    
    print("\n1. Command Line Usage:")
    print("   python3 pdf_to_excel.py document.pdf")
    print("   python3 pdf_to_excel.py document.pdf -o output.xlsx")
    print("   python3 pdf_to_excel.py document.pdf -d /path/to/output")
    
    print("\n2. Batch Conversion:")
    print("   python3 batch_convert.py /path/to/pdfs")
    print("   python3 batch_convert.py . -w 8")
    
    print("\n3. Web Interface:")
    print("   python3 web_app.py")
    print("   # Then open http://localhost:5000 in your browser")
    
    print("\n4. Python API:")
    print("   from pdf_to_excel import PDFToExcelConverter")
    print("   converter = PDFToExcelConverter()")
    print("   converter.convert_pdf_to_excel('input.pdf', 'output.xlsx')")

def main():
    """Main demo function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("PDF to Excel Converter Demo")
        print("Usage: python3 demo.py [--help]")
        print("\nOptions:")
        print("  --help    Show this help message")
        return
    
    print("🎯 This demo will:")
    print("   1. Create a sample PDF document")
    print("   2. Convert it to Excel format")
    print("   3. Show the conversion results")
    print("   4. Display usage examples")
    
    response = input("\nContinue with demo? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Demo cancelled.")
        return
    
    # Run the demo
    success = run_demo()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("You can now use the converter with your own PDF files.")
    else:
        print("\n❌ Demo failed. Please check the errors above.")
    
    # Show usage examples
    show_usage_examples()
    
    print("\n📚 For more information, see README.md")
    print("🔧 For troubleshooting, run: python3 test_converter.py")

if __name__ == "__main__":
    main()