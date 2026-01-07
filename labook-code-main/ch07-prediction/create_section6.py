#!/usr/bin/env python3
"""
Ch07 SDD Section 6: Security & Data Privacy
Fills in the Security & Data Privacy section with FERPA compliance and data handling details.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch

def create_section6_content():
    """Generate Section 6 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section6.pdf'
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
        name='SectionHeader',
        fontSize=14,
        fontName='Helvetica-Bold',
        spaceAfter=15,
        spaceBefore=20
    ))
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=10,
        spaceBefore=10
    ))

    story = []

    # Section 6: Security & Data Privacy
    story.append(Paragraph('6. Security & Data Privacy', styles['SectionHeader']))
    
    intro = """
    Given the educational context of this application, protecting student data privacy and ensuring compliance with regulations like FERPA (Family Educational Rights and Privacy Act) is paramount. This section outlines the security measures implemented in the Learning Analytics Prediction System.
    """
    story.append(Paragraph(intro, styles['Normal']))

    # 6.1 Regulatory Compliance (FERPA)
    story.append(Paragraph('6.1 Regulatory Compliance (FERPA)', styles['SubsectionHeader']))
    
    ferpa_text = """
    The system processes "education records" as defined by FERPA. To maintain compliance:
    """
    story.append(Paragraph(ferpa_text, styles['Normal']))
    
    ferpa_list = ListFlowable(
        [
            ListItem(Paragraph("**Legitimate Educational Interest:** Access to the system's inputs and outputs is strictly limited to authorized school officials (instructors, administrators) who have a legitimate educational interest in student success.", styles['Normal'])),
            ListItem(Paragraph("**Data Minimization:** Only data necessary for the prediction task (activity logs, grades) is ingested. Personally Identifiable Information (PII) such as social security numbers, addresses, or financial data is **excluded** from the pipeline.", styles['Normal'])),
            ListItem(Paragraph("**No External Sharing:** Student data is processed locally or within the institution's private cloud. No data is sent to third-party public APIs or external model training services.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(ferpa_list)

    # 6.2 Data Anonymization & Pseudonymization
    story.append(Paragraph('6.2 Data Anonymization Strategy', styles['SubsectionHeader']))
    
    anon_text = """
    To mitigate privacy risks, the system employs a strong pseudonymization strategy:
    """
    story.append(Paragraph(anon_text, styles['Normal']))
    
    anon_list = ListFlowable(
        [
            ListItem(Paragraph("**User Identification:** The system uses opaque, numeric User IDs (e.g., `12345`) rather than student names or email addresses in all internal processing tables (Events, Sessions, Features).", styles['Normal'])),
            ListItem(Paragraph("**Mapping Table separation:** The mapping table linking User IDs to real names is stored separately in a secure, access-controlled location, strictly for final reporting by the instructor. It is NOT part of the machine learning pipeline.", styles['Normal'])),
            ListItem(Paragraph("**Aggregation:** Where possible, reporting is done at the aggregate level (e.g., '30% of students are at risk') rather than exposing individual records, unless specific intervention is required.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(anon_list)

    # 6.3 Access Control
    story.append(Paragraph('6.3 Access Control Mechanisms', styles['SubsectionHeader']))
    
    access_text = """
    Access to the prediction system and its data is governed by the following roles:
    """
    story.append(Paragraph(access_text, styles['Normal']))
    
    access_list = ListFlowable(
        [
            ListItem(Paragraph("**Administrator:** Full access to configure the system, run training pipelines, and manage user roles. Can view all raw logs and prediction outputs.", styles['Normal'])),
            ListItem(Paragraph("**Instructor:** Read-only access to prediction dashboards and reports for their specific courses. Cannot modify model parameters or view raw system logs.", styles['Normal'])),
            ListItem(Paragraph("**Student:** No direct access to the prediction system. Prediction results are only shared with students at the instructor's discretion via separate feedback channels.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(access_list)

    # 6.4 Secure Data Handling
    story.append(Paragraph('6.4 Secure Data Handling', styles['SubsectionHeader']))
    
    secure_text = """
    Technical measures to ensure data security during processing and storage:
    """
    story.append(Paragraph(secure_text, styles['Normal']))
    
    secure_list = ListFlowable(
        [
            ListItem(Paragraph("**Encryption at Rest:** All sensitive input files (`Events.xlsx`, `Results.xlsx`) and serialized output files (`features.pkl`, `predictions.csv`) should be stored on encrypted file systems (e.g., BitLocker, AES-256).", styles['Normal'])),
            ListItem(Paragraph("**Pickle Security:** Python `pickle` files can execute arbitrary code. The system is configured to only load pickle files from trusted, local directories. Loading remote pickle files is disabled to prevent code injection attacks.", styles['Normal'])),
            ListItem(Paragraph("**Audit Logging:** All batch prediction runs are logged with a timestamp, initiating user, and model version used. This creates an audit trail to track who generated predictions and when.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(secure_list)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 6: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section6_content()