#!/usr/bin/env python3
"""
Ch07 Software Design Document Template Generator
Creates a comprehensive PDF template for the Learning Analytics Prediction System SDD
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_sdd_template():
    """Generate the SDD template PDF"""

    # Document setup
    pdf_path = 'Ch07_SDD_Template.pdf'
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
        name='CoverTitle',
        fontSize=24,
        fontName='Helvetica-Bold',
        alignment=1,  # Center
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontSize=18,
        fontName='Helvetica-Bold',
        alignment=1,
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='CoverInfo',
        fontSize=12,
        alignment=1,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='TOCHeader',
        fontSize=16,
        fontName='Helvetica-Bold',
        spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='TOCEntry',
        fontSize=11,
        spaceAfter=5
    ))
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

    # Cover Page
    story.append(Paragraph('Software Design Document', styles['CoverTitle']))
    story.append(Paragraph('Chapter 7: Learning Analytics Prediction System', styles['CoverSubtitle']))
    story.append(Spacer(1, 40))
    story.append(Paragraph('Final Year Project (FYP)', styles['CoverInfo']))
    story.append(Paragraph('Mustafa Hameed', styles['CoverInfo']))
    story.append(Paragraph(f'Date: {datetime.now().strftime("%B %d, %Y")}', styles['CoverInfo']))
    story.append(Paragraph('Institution: [Your Institution]', styles['CoverInfo']))
    story.append(PageBreak())

    # Abstract
    story.append(Paragraph('Abstract', styles['SectionHeader']))
    abstract_text = """
    This Software Design Document (SDD) provides a comprehensive architectural overview of the Learning Analytics Prediction System implemented in Chapter 7. The system transforms raw Moodle Learning Management System (LMS) event logs into predictive models that forecast student course outcomes and final grades. The document details the system's architecture, data models, user interfaces, design decisions, algorithms, security measures, deployment strategies, and testing approaches. The system employs advanced feature engineering techniques including sessionization, entropy-based behavioral analysis, and ensemble machine learning models to achieve predictive accuracy that improves significantly within the first two weeks of course activity.
    """
    story.append(Paragraph(abstract_text, styles['Normal']))
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph('Table of Contents', styles['TOCHeader']))

    toc_entries = [
        '1. Application Architecture',
        '2. Data Model Schema',
        '3. User Interface',
        '4. Design Decisions & Rationale',
        '5. Algorithm & Methodology',
        '6. Security & Data Privacy',
        '7. Deployment & Operations',
        '8. Testing Strategy',
        'Appendix A: Feature Dictionary',
        'Appendix B: Configuration Reference',
        'Appendix C: Code Samples & Pseudocode',
        'Appendix D: Data Samples',
        'Glossary',
        'References'
    ]

    for i, entry in enumerate(toc_entries, 1):
        story.append(Paragraph(f'{entry} ...................................................... {i+2}', styles['TOCEntry']))

    story.append(PageBreak())

    # Section 1: Application Architecture
    story.append(Paragraph('1. Application Architecture', styles['SectionHeader']))
    story.append(Paragraph('1.1 System Overview', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: System overview description]', styles['Normal']))
    story.append(Paragraph('1.2 Architecture Diagrams', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Description of context, component, and data flow diagrams]', styles['Normal']))
    story.append(Paragraph('1.3 Technology Stack', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Python 3.12, pandas, scikit-learn, etc.]', styles['Normal']))
    story.append(Paragraph('1.4 System Constraints', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Scalability, performance, data volume constraints]', styles['Normal']))
    story.append(PageBreak())

    # Section 2: Data Model Schema
    story.append(Paragraph('2. Data Model Schema', styles['SectionHeader']))
    story.append(Paragraph('2.1 Entity-Relationship Diagram', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: ERD description with 5 entities]', styles['Normal']))
    story.append(Paragraph('2.2 Table Definitions', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Events, Sessions, Features, Results, Predictions tables]', styles['Normal']))
    story.append(Paragraph('2.3 Data Relationships', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Primary keys, foreign keys, cardinality]', styles['Normal']))
    story.append(PageBreak())

    # Section 3: User Interface
    story.append(Paragraph('3. User Interface', styles['SectionHeader']))
    story.append(Paragraph('3.1 Input Specifications', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Excel file formats, required columns]', styles['Normal']))
    story.append(Paragraph('3.2 Output Specifications', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: CSV, pickle, joblib formats]', styles['Normal']))
    story.append(Paragraph('3.3 Dashboard Mockups', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Activity heatmap, prediction timeline, feature importance]', styles['Normal']))
    story.append(PageBreak())

    # Section 4: Design Decisions & Rationale
    story.append(Paragraph('4. Design Decisions & Rationale', styles['SectionHeader']))
    story.append(Paragraph('4.1 Sessionization Threshold', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Why 1.5-hour threshold for session breaks]', styles['Normal']))
    story.append(Paragraph('4.2 Model Selection', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Random Forest vs alternatives]', styles['Normal']))
    story.append(Paragraph('4.3 Feature Engineering Choices', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Entropy, session metrics rationale]', styles['Normal']))
    story.append(PageBreak())

    # Section 5: Algorithm & Methodology
    story.append(Paragraph('5. Algorithm & Methodology', styles['SectionHeader']))
    story.append(Paragraph('5.1 Feature Engineering Pipeline', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Step-by-step feature computation]', styles['Normal']))
    story.append(Paragraph('5.2 Model Training Strategy', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Week-by-week prediction approach]', styles['Normal']))
    story.append(Paragraph('5.3 Evaluation Metrics', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Accuracy, F1, RMSE, R² definitions]', styles['Normal']))
    story.append(PageBreak())

    # Section 6: Security & Data Privacy
    story.append(Paragraph('6. Security & Data Privacy', styles['SectionHeader']))
    story.append(Paragraph('6.1 Data Protection Measures', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: FERPA compliance, anonymization]', styles['Normal']))
    story.append(Paragraph('6.2 Access Control', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: User permissions, audit logging]', styles['Normal']))
    story.append(Paragraph('6.3 Privacy Considerations', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Student data sensitivity]', styles['Normal']))
    story.append(PageBreak())

    # Section 7: Deployment & Operations
    story.append(Paragraph('7. Deployment & Operations', styles['SectionHeader']))
    story.append(Paragraph('7.1 Deployment Architecture', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Batch processing pipeline]', styles['Normal']))
    story.append(Paragraph('7.2 Model Versioning', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Version tracking strategy]', styles['Normal']))
    story.append(Paragraph('7.3 Monitoring & Maintenance', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Performance monitoring, retraining]', styles['Normal']))
    story.append(PageBreak())

    # Section 8: Testing Strategy
    story.append(Paragraph('8. Testing Strategy', styles['SectionHeader']))
    story.append(Paragraph('8.1 Unit Testing', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Feature computation tests]', styles['Normal']))
    story.append(Paragraph('8.2 Integration Testing', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: End-to-end pipeline tests]', styles['Normal']))
    story.append(Paragraph('8.3 Validation Testing', styles['SubsectionHeader']))
    story.append(Paragraph('[Placeholder: Model performance benchmarks]', styles['Normal']))
    story.append(PageBreak())

    # Appendix A: Feature Dictionary
    story.append(Paragraph('Appendix A: Feature Dictionary', styles['SectionHeader']))
    story.append(Paragraph('[Placeholder: List of all 20+ engineered features with descriptions]', styles['Normal']))
    story.append(PageBreak())

    # Appendix B: Configuration Reference
    story.append(Paragraph('Appendix B: Configuration Reference', styles['SectionHeader']))
    story.append(Paragraph('[Placeholder: Configurable parameters and their values]', styles['Normal']))
    story.append(PageBreak())

    # Appendix C: Code Samples & Pseudocode
    story.append(Paragraph('Appendix C: Code Samples & Pseudocode', styles['SectionHeader']))
    story.append(Paragraph('[Placeholder: Key code snippets and pseudocode]', styles['Normal']))
    story.append(PageBreak())

    # Appendix D: Data Samples
    story.append(Paragraph('Appendix D: Data Samples', styles['SectionHeader']))
    story.append(Paragraph('[Placeholder: Sample data from each pipeline stage]', styles['Normal']))
    story.append(PageBreak())

    # Glossary
    story.append(Paragraph('Glossary', styles['SectionHeader']))
    glossary_items = [
        'Sessionization: Process of grouping user events into sessions based on time gaps',
        'Entropy: Measure of randomness or diversity in behavioral patterns',
        'Feature Engineering: Process of creating predictive features from raw data',
        'Random Forest: Ensemble machine learning algorithm using multiple decision trees',
        'FERPA: Family Educational Rights and Privacy Act for student data protection'
    ]
    for item in glossary_items:
        story.append(Paragraph(f'• {item}', styles['Normal']))
    story.append(PageBreak())

    # References
    story.append(Paragraph('References', styles['SectionHeader']))
    references = [
        'Scikit-learn Documentation. https://scikit-learn.org/',
        'Pandas Documentation. https://pandas.pydata.org/',
        'ReportLab Documentation. https://www.reportlab.com/docs/reportlab-userguide.pdf',
        'Learning Analytics Research Papers [To be added]'
    ]
    for ref in references:
        story.append(Paragraph(f'• {ref}', styles['Normal']))

    # Document Revision History
    story.append(PageBreak())
    story.append(Paragraph('Document Revision History', styles['SectionHeader']))
    revision_data = [
        ['Version', 'Date', 'Author', 'Description'],
        ['1.0', datetime.now().strftime('%Y-%m-%d'), 'Mustafa Hameed', 'Initial SDD template creation']
    ]
    revision_table = Table(revision_data)
    revision_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT')
    ]))
    story.append(revision_table)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created SDD template: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_sdd_template()