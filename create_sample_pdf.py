#!/usr/bin/env python3
"""
Create a sample PDF with table data for testing the PDF to Excel converter.
"""

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

def create_sample_pdf():
    """Create a sample PDF with tables and text for testing."""
    filename = "sample_data.pdf"
    
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Add title
    title = Paragraph("Sample Data Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add description
    description = Paragraph("This is a sample PDF containing tables and structured data for testing the PDF to Excel converter.", styles['Normal'])
    story.append(description)
    story.append(Spacer(1, 12))
    
    # Sample table 1: Sales Data
    story.append(Paragraph("Sales Data Q1 2024", styles['Heading2']))
    sales_data = [
        ['Month', 'Product', 'Units Sold', 'Revenue', 'Profit'],
        ['January', 'Widget A', '150', '$15,000', '$4,500'],
        ['January', 'Widget B', '200', '$30,000', '$12,000'],
        ['February', 'Widget A', '175', '$17,500', '$5,250'],
        ['February', 'Widget B', '225', '$33,750', '$13,500'],
        ['March', 'Widget A', '200', '$20,000', '$6,000'],
        ['March', 'Widget B', '250', '$37,500', '$15,000']
    ]
    
    sales_table = Table(sales_data)
    sales_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(sales_table)
    story.append(Spacer(1, 24))
    
    # Sample table 2: Employee Data
    story.append(Paragraph("Employee Information", styles['Heading2']))
    employee_data = [
        ['Employee ID', 'Name', 'Department', 'Salary', 'Start Date'],
        ['EMP001', 'John Smith', 'Engineering', '$75,000', '2020-01-15'],
        ['EMP002', 'Jane Doe', 'Marketing', '$65,000', '2019-03-22'],
        ['EMP003', 'Mike Johnson', 'Sales', '$70,000', '2021-06-10'],
        ['EMP004', 'Sarah Wilson', 'HR', '$60,000', '2018-11-05'],
        ['EMP005', 'David Brown', 'Engineering', '$80,000', '2020-09-18']
    ]
    
    employee_table = Table(employee_data)
    employee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(employee_table)
    story.append(Spacer(1, 24))
    
    # Add some key-value data
    story.append(Paragraph("Summary Information", styles['Heading2']))
    summary_text = """
    Total Revenue: $153,750
    Total Profit: $56,250
    Best Performing Product: Widget B
    Top Sales Month: March
    Average Employee Salary: $70,000
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print(f"Sample PDF created: {filename}")
    return filename

if __name__ == "__main__":
    # Try to install reportlab if not available
    try:
        import reportlab
    except ImportError:
        import subprocess
        import sys
        print("Installing reportlab...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        import reportlab
    
    create_sample_pdf()