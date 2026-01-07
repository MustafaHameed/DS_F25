#!/usr/bin/env python3
"""
Ch07 SDD Section 8: Testing Strategy
Fills in the Testing Strategy section with unit, integration, and validation test plans.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.units import inch

def create_section8_content():
    """Generate Section 8 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section8.pdf'
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

    # Section 8: Testing Strategy
    story.append(Paragraph('8. Testing Strategy', styles['SectionHeader']))
    
    intro = """
    Reliability is critical for an educational support system. This section defines the comprehensive testing strategy, covering code correctness (Units), pipeline integrity (Integration), and model efficacy (Validation).
    """
    story.append(Paragraph(intro, styles['Normal']))

    # 8.1 Unit Testing
    story.append(Paragraph('8.1 Unit Testing Strategy', styles['SubsectionHeader']))
    story.append(Paragraph('Unit tests focus on validating the logic of individual transformation functions using the `pytest` framework.', styles['Normal']))
    
    unit_tests = [
        ['Component', 'Test Case Identifier', 'Description', 'Expected Outcome'],
        ['Feature Eng', 'UT-FE-001: Entropy Zero', 'Calculate entropy for single-value list [A, A, A]', 'Entropy = 0.0'],
        ['Feature Eng', 'UT-FE-002: Entropy Max', 'Calculate entropy for uniform list [A, B, C]', 'Entropy = 1.58 (log2(3))'],
        ['Sessionization', 'UT-SESS-001: Gap Splitting', '2 events with 1h 40m gap', 'Returns 2 distinct session IDs'],
        ['Sessionization', 'UT-SESS-002: Gap Merging', '2 events with 1h 20m gap', 'Returns 1 same session ID'],
        ['Preprocessing', 'UT-PRE-001: Invalid Date', 'Input event with date "2023-13-45"', 'Raises ValueError or filters row'],
    ]
    
    t_unit = Table(unit_tests, colWidths=[1*inch, 1.5*inch, 2.5*inch, 1.5*inch])
    t_unit.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_unit)

    # 8.2 Integration Testing
    story.append(Paragraph('8.2 Integration Testing Strategy', styles['SubsectionHeader']))
    
    integ_text = """
    Integration tests verify that data flows correctly between the six core components of the pipeline.
    """
    story.append(Paragraph(integ_text, styles['Normal']))
    
    integ_list = ListFlowable(
        [
            ListItem(Paragraph('**IT-PIPE-001 (End-to-End Smoke Test):** Run the complete pipeline on a small "Golden Dataset" (10 users, 500 events). Verify that `predictions.csv` is generated and contains exactly 10 rows.', styles['Normal'])),
            ListItem(Paragraph("**IT-DATA-001 (Schema Compatibility):** Verify that the output of the Feature Engineering component matches the input schema expected by the Model Training component (column names and types).", styles['Normal'])),
            ListItem(Paragraph("**IT-IO-001 (Persistence):** Verify that a model saved to disk using `joblib` can be loaded and produce identical predictions to the in-memory model object.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(integ_list)

    # 8.3 Model Validation
    story.append(Paragraph('8.3 Model Validation Strategy', styles['SubsectionHeader']))
    
    valid_text = """
    Model validation ensures the predictive performance remains acceptable for real-world use.
    """
    story.append(Paragraph(valid_text, styles['Normal']))

    valid_list = ListFlowable(
        [
            ListItem(Paragraph("**Acceptance Criteria:** The model must achieve an F1-score > 0.65 on the hold-out validation set for Weeks 3-5 before deployment.", styles['Normal'])),
            ListItem(Paragraph('**Baseline Comparison:** The model must outperform a "Dummy Classifier" (Strategy: Most Frequent) by at least 15% in Accuracy.', styles['Normal'])),
            ListItem(Paragraph("**Bias Check:** False Negative Rate (FNR) should be roughly equal across student activity quartiles to ensure the model doesn't systematically ignore low-activity students.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(valid_list)

    # 8.4 Test Data Management
    story.append(Paragraph('8.4 Test Data Management', styles['SubsectionHeader']))
    
    data_text = """
    To support reproducible testing, the following datasets are maintained in the `/tests/data/` directory:
    - **`golden_events_v1.xlsx`**: A curated set of 500 events covering all edge cases (long gaps, rapid clicks, weird dates).
    - **`expected_features_v1.pkl`**: The verified correct feature vectors corresponding to the golden events.
    - **`regression_test_model.joblib`**: A frozen version of the model to test for backward compatibility of feature generation code.
    """
    story.append(Paragraph(data_text, styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 8: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section8_content()