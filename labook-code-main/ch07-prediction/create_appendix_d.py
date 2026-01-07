#!/usr/bin/env python3
"""
Ch07 SDD Appendix D: Data Samples
Fills in Appendix D with sample data rows.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_appendix_d_content():
    """Generate Appendix D content for SDD"""

    # Document setup - Landscape for wide data tables
    pdf_path = 'Ch07_SDD_Appendix_D.pdf'
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
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

    # Appendix D
    story.append(Paragraph('Appendix D: Data Samples', styles['AppendixHeader']))
    story.append(Paragraph('This appendix provides snapshots of the data at various stages of the pipeline to illustrate the transformations.', styles['Normal']))
    story.append(Spacer(1, 15))

    # 1. Raw Events
    story.append(Paragraph('1. Raw Events (Input)', styles['SectionHeader']))
    
    events_data = [
        ['user', 'ts', 'action', 'week'],
        ['1001', '2023-09-01 10:15:00', 'view', '1'],
        ['1001', '2023-09-01 10:15:30', 'view', '1'],
        ['1001', '2023-09-01 10:20:00', 'post', '1'],
        ['1002', '2023-09-02 14:00:00', 'view', '1'],
        ['1003', '2023-09-03 09:00:00', 'submit', '1']
    ]
    
    t_events = Table(events_data, colWidths=[1*inch, 2.5*inch, 1.5*inch, 1*inch])
    t_events.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_events)
    story.append(Spacer(1, 20))

    # 2. Processed Sessions
    story.append(Paragraph('2. Processed Sessions (Intermediate)', styles['SectionHeader']))
    
    sess_data = [
        ['session_id', 'user', 'start', 'end', 'len (s)', 'events'],
        ['1001_s1', '1001', '2023-09-01 10:15:00', '2023-09-01 10:20:00', '300.0', '3'],
        ['1002_s1', '1002', '2023-09-02 14:00:00', '2023-09-02 14:00:00', '0.0', '1'],
        ['1003_s1', '1003', '2023-09-03 09:00:00', '2023-09-03 09:00:00', '0.0', '1']
    ]
    
    t_sess = Table(sess_data, colWidths=[1.5*inch, 1*inch, 2*inch, 2*inch, 1*inch, 1*inch])
    t_sess.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_sess)
    story.append(Spacer(1, 20))

    # 3. Computed Features
    story.append(Paragraph('3. Computed Features (Model Input)', styles['SectionHeader']))
    story.append(Paragraph('*Subset of columns shown for brevity*', styles['Normal']))
    
    feat_data = [
        ['user', 'avg_daily', 'entropy_day', 'med_sess_len', 'sess_cnt', 'active_days'],
        ['1001', '3.0', '1.58', '300.0', '1', '1'],
        ['1002', '0.5', '0.0', '0.0', '1', '1'],
        ['1003', '10.5', '2.32', '1250.0', '5', '3'],
        ['1004', '0.0', '0.0', '0.0', '0', '0']
    ]
    
    t_feat = Table(feat_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    t_feat.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 20))

    # 4. Predictions
    story.append(Paragraph('4. Predictions (Output)', styles['SectionHeader']))
    
    pred_data = [
        ['user', 'week', 'pred_outcome', 'prob', 'pred_grade', 'model_ver'],
        ['1001', '2', 'High', '0.78', '85.4', 'v1.1'],
        ['1002', '2', 'Low', '0.35', '62.1', 'v1.1'],
        ['1003', '2', 'High', '0.92', '91.0', 'v1.1'],
        ['1004', '2', 'Low', '0.12', '45.0', 'v1.1']
    ]
    
    t_pred = Table(pred_data, colWidths=[1*inch, 1*inch, 1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    t_pred.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t_pred)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Appendix D: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_appendix_d_content()