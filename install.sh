#!/bin/bash

# PDF to Excel Converter Installation Script
# This script installs all dependencies and sets up the converter

set -e

echo "🚀 PDF to Excel Converter - Installation Script"
echo "================================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ pip3 is available"

# Upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check system dependencies
echo "🔍 Checking system dependencies..."

# Check Java (required for tabula-py)
if ! command -v java &> /dev/null; then
    echo "⚠️  Java is not installed. tabula-py functionality will be limited."
    echo "   To install Java on Ubuntu/Debian: sudo apt-get install default-jre"
    echo "   To install Java on CentOS/RHEL: sudo yum install java-1.8.0-openjdk"
    echo "   To install Java on macOS: brew install openjdk"
else
    echo "✅ Java is available"
fi

# Check OpenCV dependencies (required for camelot-py)
if command -v apt-get &> /dev/null; then
    echo "📦 Installing OpenCV dependencies for Ubuntu/Debian..."
    sudo apt-get update
    sudo apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1
elif command -v yum &> /dev/null; then
    echo "📦 Installing OpenCV dependencies for CentOS/RHEL..."
    sudo yum install -y \
        mesa-libGL \
        glib2 \
        libSM \
        libXext \
        libXrender
elif command -v brew &> /dev/null; then
    echo "📦 Installing OpenCV dependencies for macOS..."
    brew install opencv
else
    echo "⚠️  Package manager not detected. Please install OpenCV dependencies manually."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p output
mkdir -p templates

# Test the installation
echo "🧪 Testing the installation..."
python3 test_converter.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "📖 Usage:"
    echo "  Command line: python3 pdf_to_excel.py document.pdf"
    echo "  Web interface: python3 web_app.py"
    echo "  Batch conversion: python3 batch_convert.py /path/to/pdfs"
    echo ""
    echo "🌐 Web interface will be available at: http://localhost:5000"
    echo ""
    echo "📚 For more information, see README.md"
else
    echo ""
    echo "❌ Installation test failed. Please check the errors above."
    exit 1
fi