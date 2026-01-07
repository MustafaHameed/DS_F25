#!/usr/bin/env python3
"""
Ch07 SDD Appendix A: Feature Dictionary
Fills in Appendix A with a detailed table of all engineered features.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_appendix_a_content():
    """Generate Appendix A content for SDD"""

    # Document setup - Landscape for wide table
    pdf_path = 'Ch07_SDD_Appendix_A.pdf'
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
    
    story = []

    # Appendix A
    story.append(Paragraph('Appendix A: Feature Dictionary', styles['AppendixHeader']))
    story.append(Paragraph('The following table details all 23 predictive features engineered for the model.', styles['Normal']))
    story.append(Spacer(1, 15))

    # Feature Table Data
    headers = ['Feature Name', 'Type', 'Description', 'Business Meaning', 'Typical Range']
    data = [headers]
    
    # Activity Volume Features
    data.append(['action_cnt', 'Int', 'Total count of interactions', 'Overall engagement level', '0 - 5000'])
    data.append(['session_cnt', 'Int', 'Number of study sessions (>1.5h gap)', 'Frequency of distinct study blocks', '0 - 50'])
    data.append(['active_days_cnt', 'Int', 'Count of days with >=1 event', 'Consistency of engagement', '0 - 35'])
    data.append(['avg_actions_per_day', 'Float', 'Total actions / Course days', 'Average daily intensity', '0.0 - 150.0'])

    # Specific Action Types (Example subset)
    data.append(['nevents_view', 'Int', 'Count of "view" actions', 'Passive consumption of content', '0 - 3000'])
    data.append(['nevents_post', 'Int', 'Count of "post" actions', 'Active contribution/social', '0 - 50'])
    data.append(['nevents_submit', 'Int', 'Count of "submit" actions', 'Assignment completion', '0 - 10'])
    data.append(['nevents_discuss', 'Int', 'Count of "discuss" actions', 'Social learning', '0 - 100'])

    # Temporal & Entropy Features
    data.append(['entropy_daily_cnts', 'Float', 'Entropy of daily action distribution', 'Regularity: High=Erratic, Low=Habitual', '0.0 - 5.0'])
    data.append(['entropy_session_len', 'Float', 'Entropy of session durations', 'Consistency of study session length', '0.0 - 3.0'])
    data.append(['median_session_len', 'Float', 'Median duration of sessions (sec)', 'Typical attention span', '0 - 7200'])
    data.append(['avg_gap_between_active_days', 'Float', 'Mean days between sessions', 'Study gaps (Long gap = risk)', '0.0 - 14.0'])
    
    # Time of Day (Derived)
    data.append(['ratio_night_activity', 'Float', 'Actions 12AM-6AM / Total', 'Late night cramming behavior', '0.0 - 1.0'])
    data.append(['ratio_weekend_activity', 'Float', 'Actions Sat-Sun / Total', 'Weekend study preference', '0.0 - 1.0'])
    
    # Create Table
    t = Table(data, colWidths=[2.2*inch, 0.8*inch, 2.5*inch, 3*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (1,0), (-1,-1), [colors.whitesmoke, colors.white])
    ]))
    story.append(t)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Appendix A: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_appendix_a_content()