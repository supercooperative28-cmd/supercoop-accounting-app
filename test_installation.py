#!/usr/bin/env python3
"""
Test script to verify PDF to Excel converter installation
Run this script to check if all dependencies are properly installed.
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        if package_name:
            importlib.import_module(module_name, package_name)
        else:
            importlib.import_module(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def main():
    """Test all required dependencies."""
    print("PDF to Excel Converter - Installation Test")
    print("=" * 50)
    
    # Required packages
    required_packages = [
        ("pandas", "pandas"),
        ("pdfplumber", "pdfplumber"),
        ("tabula", "tabula"),
        ("camelot", "camelot"),
        ("PyPDF2", "PyPDF2"),
        ("openpyxl", "openpyxl"),
        ("flask", "flask"),
        ("werkzeug", "werkzeug"),
    ]
    
    all_good = True
    
    print("\nTesting Python packages...")
    for display_name, import_name in required_packages:
        success, error = test_import(import_name)
        if success:
            print(f"✅ {display_name}")
        else:
            print(f"❌ {display_name}: {error}")
            all_good = False
    
    print("\n" + "=" * 50)
    
    # Test system dependencies
    print("\nTesting system dependencies...")
    
    # Test Java (required for tabula)
    try:
        import subprocess
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Java Runtime Environment (JRE)")
        else:
            print("❌ Java Runtime Environment (JRE) - not working properly")
            all_good = False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Java Runtime Environment (JRE) - not found")
        all_good = False
    
    # Test Ghostscript (required for camelot)
    try:
        result = subprocess.run(['gs', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ghostscript")
        else:
            print("❌ Ghostscript - not working properly")
            all_good = False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ghostscript - not found")
        all_good = False
    
    print("\n" + "=" * 50)
    
    # Test local modules
    print("\nTesting local modules...")
    
    try:
        from pdf_to_excel import PDFToExcelConverter
        print("✅ PDF to Excel converter module")
    except ImportError as e:
        print(f"❌ PDF to Excel converter module: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    
    # Summary
    if all_good:
        print("\n🎉 All tests passed! Your installation is ready.")
        print("\nYou can now:")
        print("  - Use the command line tool: python pdf_to_excel.py your_file.pdf")
        print("  - Run the web interface: python web_app.py")
        print("  - Try the examples: python example_usage.py")
    else:
        print("\n⚠️  Some tests failed. Please install missing dependencies:")
        print("\nFor Python packages:")
        print("  pip install -r requirements.txt")
        print("\nFor system dependencies:")
        print("  Ubuntu/Debian: sudo apt-get install default-jre ghostscript")
        print("  CentOS/RHEL: sudo yum install java-11-openjdk ghostscript")
        print("  macOS: brew install openjdk ghostscript")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()