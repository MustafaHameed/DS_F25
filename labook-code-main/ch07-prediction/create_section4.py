#!/usr/bin/env python3
"""
Ch07 SDD Section 4: Design Decisions & Rationale
Fills in the Design Decisions section with justifications for algorithm choices and parameters.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch

def create_section4_content():
    """Generate Section 4 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section4.pdf'
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

    # Section 4: Design Decisions & Rationale
    story.append(Paragraph('4. Design Decisions & Rationale', styles['SectionHeader']))
    
    intro = """
    This section documents the key architectural and algorithmic decisions made during the design of the Learning Analytics Prediction System. Each decision is justified based on the specific characteristics of educational data and the project requirements.
    """
    story.append(Paragraph(intro, styles['Normal']))

    # 4.1 Data Processing Decisions
    story.append(Paragraph('4.1 Data Processing Decisions', styles['SubsectionHeader']))
    
    # Sessionization Threshold
    story.append(Paragraph('4.1.1 Sessionization Threshold (1.5 Hours)', styles['SubsectionHeader']))
    session_text = """
    **Decision:** A 1.5-hour (90-minute) inactivity threshold was selected to delimit student study sessions.
    
    **Rationale:** 
    1.  **Literature Alignment:** Educational psychology research suggests that typical continuous study blocks rarely exceed 90 minutes without a break.
    2.  **Contextual Appropriateness:** For online Moodle interactions, a very short threshold (e.g., 15 mins) would over-segment fragmented browsing, while a very long one (e.g., 4 hours) would incorrectly merge distinct study periods (e.g., morning and afternoon sessions).
    3.  **Empirical Validation:** Preliminary analysis of the event logs showed a bimodal distribution of time gaps, where the 1.5-hour cut-off effectively separated "within-session" pauses from "between-session" breaks.
    """
    story.append(Paragraph(session_text, styles['Normal']))

    # 4.2 Feature Engineering Decisions
    story.append(Paragraph('4.2 Feature Engineering Decisions', styles['SubsectionHeader']))

    # Entropy Features
    story.append(Paragraph('4.2.1 Use of Entropy for Behavioral Consistency', styles['SubsectionHeader']))
    entropy_text = """
    **Decision:** Shannon Entropy was utilized to quantify the regularity of student study habits (e.g., `entropy_daily_cnts`, `entropy_session_len`).
    
    **Rationale:**
    1.  **Capturing Distribution:** Simple metrics like "average actions" mask the valid distribution. Two students might have the same average but completely different consistency.
    2.  **Behavioral Signal:** Low entropy indicates highly regular, habitual study patterns, while high entropy indicates erratic or cramming behavior. This provides a distinct predictive signal that complements magnitude-based features.
    """
    story.append(Paragraph(entropy_text, styles['Normal']))
    
    # 4.3 Modeling Decisions
    story.append(Paragraph('4.3 Modeling Decisions', styles['SubsectionHeader']))

    # Random Forest vs OLS
    story.append(Paragraph('4.3.1 Model Selection: Random Forest Classification/Regression', styles['SubsectionHeader']))
    rf_text = """
    **Decision:** Random Forest (RF) was chosen as the primary modeling algorithm over linear alternatives like OLS Regression or Logistic Regression.
    
    **Rationale:**
    1.  **Non-Linearity:** Student behavioral data is inherently non-linear. For example, the relationship between "session length" and "grade" is often diminishing returns—studying 10 hours is better than 1, but studying 20 hours might validly be worse due to burnout. Linear models struggle to capture this.
    2.  **Interaction Effects:** Success often depends on combinations of behaviors (e.g., high activity + high consistency). RF inherently captures these high-order interactions without manual feature interaction engineering.
    3.  **Robustness to Outliers:** Educational data often contains significant outliers (e.g., a "super-user" with 10x normal activity). RF is more robust to these outliers compared to linear models which can be skewed by them.
    """
    story.append(Paragraph(rf_text, styles['Normal']))

    # Median Split
    story.append(Paragraph('4.3.2 Outcome Definition: Median Split', styles['SubsectionHeader']))
    split_text = """
    **Decision:** For the classification task (Predicting High/Low performance), the target variable was defined using a median split of the final grades.
    
    **Rationale:**
    1.  **Class Balance:** Using a fixed threshold (e.g., >70%) often results in imbalanced classes if the course was too easy or too hard. A median split guarantees a perfectly balanced 50/50 dataset, maximizing the information available for the model to learn the boundary between "better half" and "worse half."
    2.  **Relative Performance:** In many educational contexts, relative standing (being in the top half) is a more robust indicator of student capability than absolute raw score, which varies by exam difficulty.
    """
    story.append(Paragraph(split_text, styles['Normal']))

    # 4.4 Assumptions
    story.append(Paragraph('4.4 System Assumptions', styles['SubsectionHeader']))
    assumptions_text = """
    The system design relies on the following key assumptions:
    """
    story.append(Paragraph(assumptions_text, styles['Normal']))
    
    assumptions_list = ListFlowable(
        [
            ListItem(Paragraph("**Completeness of Data:** Moodle logs capture the majority of student learning activity. Offline study (reading textbooks, peer discussions) is assumed to correlate with online activity.", styles['Normal'])),
            ListItem(Paragraph("**Temporal consistency:** The course structure (weekly modules) remains relatively consistent. Drastic changes in course design mid-semester would invalidate the 'week-by-week' prediction model.", styles['Normal'])),
            ListItem(Paragraph("**Stationarity:** The relationship between student behavior and outcomes is assumed to be stable enough that a model trained on previous weeks/years can generalize to the current cohort.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(assumptions_list)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 4: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section4_content()