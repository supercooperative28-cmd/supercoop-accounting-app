#!/usr/bin/env python3
"""
Web Application for PDF to Excel Conversion
A Flask-based web interface for converting PDF files to Excel format.
"""

import os
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pdf_to_excel import PDFToExcelConverter
import tempfile
import shutil

# Configure Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and conversion."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Convert PDF to Excel
        converter = PDFToExcelConverter(app.config['OUTPUT_FOLDER'])
        output_filename = f"{Path(filename).stem}_converted.xlsx"
        output_path = converter.convert_pdf_to_excel(filepath, output_filename)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # Return success response with download link
        download_url = url_for('download_file', filename=output_filename)
        
        return jsonify({
            'success': True,
            'message': 'PDF successfully converted to Excel!',
            'download_url': download_url,
            'filename': output_filename
        })
        
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download converted Excel file."""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)