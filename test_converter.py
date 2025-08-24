#!/usr/bin/env python3
"""
Test script for PDF to Excel Converter
This script tests the basic functionality and dependencies.
"""

import sys
import os
from pathlib import Path

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("🔍 Testing dependencies...")
    
    dependencies = [
        ('pdfplumber', 'PDF text and table extraction'),
        ('tabula', 'Table extraction from PDFs'),
        ('camelot', 'Advanced table extraction'),
        ('PyPDF2', 'PDF text extraction'),
        ('pandas', 'Data manipulation'),
        ('openpyxl', 'Excel file creation'),
        ('flask', 'Web framework')
    ]
    
    missing_deps = []
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description}")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True

def test_converter_class():
    """Test the PDFToExcelConverter class."""
    print("\n🔍 Testing converter class...")
    
    try:
        from pdf_to_excel import PDFToExcelConverter
        
        # Test class instantiation
        converter = PDFToExcelConverter("test_output")
        print("✅ PDFToExcelConverter class instantiated successfully")
        
        # Test output directory creation
        if converter.output_dir.exists():
            print("✅ Output directory created successfully")
        else:
            print("❌ Output directory creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Converter class test failed: {e}")
        return False

def test_web_app():
    """Test the web application."""
    print("\n🔍 Testing web application...")
    
    try:
        from web_app import app
        
        # Test Flask app creation
        if app and hasattr(app, 'route'):
            print("✅ Flask application created successfully")
            return True
        else:
            print("❌ Flask application creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Web application test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'pdf_to_excel.py',
        'web_app.py',
        'requirements.txt',
        'README.md',
        'templates/index.html'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n✅ All required files are present!")
    return True

def create_sample_pdf():
    """Create a sample PDF for testing."""
    print("\n🔍 Creating sample PDF for testing...")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        sample_pdf = "sample.pdf"
        c = canvas.Canvas(sample_pdf, pagesize=letter)
        
        # Add some text
        c.drawString(100, 750, "Sample PDF Document")
        c.drawString(100, 700, "This is a test document for the PDF to Excel converter.")
        
        # Add a simple table structure
        c.drawString(100, 650, "Name:")
        c.drawString(200, 650, "John Doe")
        c.drawString(100, 620, "Age:")
        c.drawString(200, 620, "30")
        c.drawString(100, 590, "City:")
        c.drawString(200, 590, "New York")
        
        c.save()
        print(f"✅ Sample PDF created: {sample_pdf}")
        return sample_pdf
        
    except ImportError:
        print("⚠️  reportlab not installed, skipping sample PDF creation")
        return None
    except Exception as e:
        print(f"❌ Sample PDF creation failed: {e}")
        return None

def main():
    """Run all tests."""
    print("🚀 PDF to Excel Converter - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("File Structure", test_file_structure),
        ("Converter Class", test_converter_class),
        ("Web Application", test_web_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    # Create sample PDF if possible
    sample_pdf = create_sample_pdf()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The converter is ready to use.")
        
        if sample_pdf:
            print(f"\n💡 You can test the converter with the sample PDF:")
            print(f"   Command line: python pdf_to_excel.py {sample_pdf}")
            print(f"   Web interface: python web_app.py")
        
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()