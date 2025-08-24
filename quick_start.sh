#!/bin/bash

# PDF to Excel Converter - Quick Start Script
# This script helps you get started quickly with the PDF to Excel converter

echo "🚀 PDF to Excel Converter - Quick Start"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check system dependencies
echo ""
echo "🔍 Checking system dependencies..."

# Check Java
if command -v java &> /dev/null; then
    echo "✅ Java Runtime Environment (JRE) found"
else
    echo "⚠️  Java Runtime Environment (JRE) not found"
    echo "   Please install Java:"
    echo "   Ubuntu/Debian: sudo apt-get install default-jre"
    echo "   CentOS/RHEL: sudo yum install java-11-openjdk"
    echo "   macOS: brew install openjdk"
fi

# Check Ghostscript
if command -v gs &> /dev/null; then
    echo "✅ Ghostscript found"
else
    echo "⚠️  Ghostscript not found"
    echo "   Please install Ghostscript:"
    echo "   Ubuntu/Debian: sudo apt-get install ghostscript"
    echo "   CentOS/RHEL: sudo yum install ghostscript"
    echo "   macOS: brew install ghostscript"
fi

# Test the installation
echo ""
echo "🧪 Testing installation..."
python3 test_installation.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📖 Usage:"
echo "   Command line: python3 pdf_to_excel.py your_file.pdf"
echo "   Web interface: python3 web_app.py"
echo "   Examples: python3 example_usage.py"
echo ""
echo "🌐 Web interface will be available at: http://localhost:5000"
echo ""
echo "💡 Tip: Run 'python3 test_installation.py' anytime to verify your setup"