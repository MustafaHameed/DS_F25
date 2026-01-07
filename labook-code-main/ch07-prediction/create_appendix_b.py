#!/usr/bin/env python3
"""
Ch07 SDD Appendix B: Configuration Reference
Fills in Appendix B with system configuration variables.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_appendix_b_content():
    """Generate Appendix B content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Appendix_B.pdf'
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='AppendixHeader',
        fontSize=16,
        fontName='Helvetica-Bold',
        spaceAfter=15,
        spaceBefore=20
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=10,
        spaceBefore=10
    ))
    
    story = []

    # Appendix B
    story.append(Paragraph('Appendix B: Configuration Reference', styles['AppendixHeader']))
    story.append(Paragraph('The system behavior is controlled by the following configuration parameters, typically defined in a `config.py` file or environment variables.', styles['Normal']))
    story.append(Spacer(1, 15))

    # 1. Pipeline Parameters
    story.append(Paragraph('1. Pipeline Parameters', styles['SectionHeader']))
    
    pipe_data = [
        ['Parameter', 'Default', 'Description'],
        ['SESSION_THRESHOLD_MINUTES', '90', 'Inactivity gap to delimit sessions (1.5 hours)'],
        ['MAX_PREDICTION_WEEK', '5', 'The final week for which predictions are generated'],
        ['MIN_EVENTS_THRESHOLD', '10', 'Minimum events required for a student to be processed'],
        ['FEATURE_SELECTION_MODE', 'all', 'Method for feature subsetting ("all", "top_10", "rfe")']
    ]
    
    t_pipe = Table(pipe_data, colWidths=[2.5*inch, 1*inch, 3*inch])
    t_pipe.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_pipe)
    
    # 2. Model Hyperparameters
    story.append(Paragraph('2. Random Forest Hyperparameters', styles['SectionHeader']))
    
    rf_data = [
        ['Parameter', 'Default', 'Description'],
        ['RF_N_ESTIMATORS', '200', 'Number of trees in the forest'],
        ['RF_MAX_DEPTH', 'None', 'Maximum depth of the tree'],
        ['RF_RANDOM_STATE', '2023', 'Seed for reproducibility'],
        ['RF_CLASS_WEIGHT', 'balanced', 'Weights associated with classes (High/Low)'],
        ['RF_CRITERION', 'gini', 'Function to measure quality of a split']
    ]
    
    t_rf = Table(rf_data, colWidths=[2.5*inch, 1*inch, 3*inch])
    t_rf.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_rf)
    
    # 3. File Paths
    story.append(Paragraph('3. File System paths', styles['SectionHeader']))
    
    path_data = [
        ['Variable', 'Default Path', 'Description'],
        ['DATA_DIR', './data/', 'Root directory for all data files'],
        ['INPUT_EVENTS', 'Events.xlsx', 'Raw Moodle event log inputs'],
        ['INPUT_RESULTS', 'Results.xlsx', 'Student grade result inputs'],
        ['OUTPUT_MODELS', './models/', 'Directory to save .joblib model files'],
        ['OUTPUT_PREDICTIONS', './predictions/', 'Directory to save predictions.csv']
    ]
    
    t_path = Table(path_data, colWidths=[2*inch, 2*inch, 2.5*inch])
    t_path.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_path)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Appendix B: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_appendix_b_content()