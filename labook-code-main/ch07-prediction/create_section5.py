#!/usr/bin/env python3
"""
Ch07 SDD Section 5: Algorithm & Methodology
Fills in the Algorithm & Methodology section with feature engineering formulas and model training details.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch

def create_section5_content():
    """Generate Section 5 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section5.pdf'
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
    styles.add(ParagraphStyle(
        name='Formula',
        fontSize=10,
        fontName='Courier',
        alignment=1, # Center
        spaceAfter=10,
        spaceBefore=10,
        leftIndent=20,
        rightIndent=20,
        backColor=colors.whitesmoke,
        borderPadding=5
    ))

    story = []

    # Section 5: Algorithm & Methodology
    story.append(Paragraph('5. Algorithm & Methodology', styles['SectionHeader']))
    story.append(Paragraph('This section details the core algorithms used for data transformation, feature computation, and model training.', styles['Normal']))

    # 5.1 Data Preprocessing & Sessionization
    story.append(Paragraph('5.1 Data Preprocessing & Sessionization', styles['SubsectionHeader']))
    
    preprocess_text = """
    Raw event logs are processed to group individual actions into learning sessions. A session is defined as a sequence of student actions with no gap longer than 1.5 hours (5400 seconds).
    """
    story.append(Paragraph(preprocess_text, styles['Normal']))
    
    # Sessionization Algorithm Step-by-Step
    story.append(Paragraph('**Algorithm 1: Session Identification**', styles['Normal']))
    session_algo_steps = """
    1. Sort events by User ($u$) and Timestamp ($t$).
    2. Calculate time difference $\Delta t_i = t_i - t_{i-1}$ for each event $i$.
    3. Initialize $SessionID = 0$.
    4. For each event $i$:
        If $\Delta t_i > 1.5$ hours (5400s) OR $User_i \neq User_{i-1}$:
            $SessionID \leftarrow SessionID + 1$
        Assign $SessionID$ to event $i$.
    5. Aggregate events by $SessionID$ to compute start/end times and total duration.
    """
    # Using Replace to simulate new lines in paragraph without multiple Paragraph objects
    story.append(Paragraph(session_algo_steps.replace('\n', '<br/>'), styles['Normal']))

    # 5.2 Feature Engineering
    story.append(Paragraph('5.2 Feature Engineering', styles['SubsectionHeader']))
    story.append(Paragraph('A total of 20+ features are computed per student, capturing different dimensions of learning behavior.', styles['Normal']))

    # 5.2.1 Activity Volume
    story.append(Paragraph('5.2.1 Activity Volume Features', styles['SubsectionHeader']))
    story.append(Paragraph('Measures the magnitude of student engagement.', styles['Normal']))
    
    vol_text = """
    - **Action Counts ($C_{action}$)**: Total count of specific action types (e.g., View, Post).
    - **Total Sessions ($N_{sessions}$)**: Count of unique study sessions.
    - **Active Days ($N_{days}$)**: Count of unique calendar days with at least one event.
    """
    story.append(Paragraph(vol_text, styles['Normal']))
    story.append(Paragraph('avg_actions_per_day = Total Actions / Total Course Duration (Days)', styles['Formula']))

    # 5.2.2 Behavioral Consistency (Entropy)
    story.append(Paragraph('5.2.2 Behavioral Consistency Features (Entropy)', styles['SubsectionHeader']))
    entropy_desc = """
    Shannon Entropy is used to measure the regularity of student behavior. High entropy implies uniform distribution (consistent), low entropy implies peaky distribution (cramming).
    """
    story.append(Paragraph(entropy_desc, styles['Normal']))
    
    story.append(Paragraph('H(X) = - \sum_{i=1}^{n} P(x_i) \log_2 P(x_i)', styles['Formula']))
    
    entropy_ex = """
    Where $P(x_i)$ is the probability (frequency) of activity in bin $i$.
    - **Daily Entropy ($H_{daily}$)**: Bins = Days of the course. $P(day_i) = \frac{Actions_{day_i}}{TotalActions}$.
    - **Session Entropy ($H_{session}$)**: Bins = Discretized session lengths.
    """
    story.append(Paragraph(entropy_ex, styles['Normal']))

    # 5.2.3 Temporal Features
    story.append(Paragraph('5.2.3 Temporal Features', styles['SubsectionHeader']))
    temp_text = """
    - **Median Session Length**: Median duration of all student sessions.
    - **Average Gap Between Active Days**: Mean time (in days) between consecutive active days.
    """
    story.append(Paragraph(temp_text, styles['Normal']))

    # 5.3 Model Training Strategy
    story.append(Paragraph('5.3 Model Training Strategy', styles['SubsectionHeader']))
    
    training_points = """
    The system employs a **Rolling Window Training** strategy to simulate a real-world semester.
    
    - **Week 1 Model**: Train on Week 1 data, Predict Week 2.
    - **Week N Model**: Train on cumulative data (Weeks 1 to N), Predict Week N+1.
    """
    story.append(Paragraph(training_points, styles['Normal']))

    # 5.3.1 Algorithm Selection
    story.append(Paragraph('5.3.1 Algorithm Selection & Hyperparameters', styles['SubsectionHeader']))
    
    rf_params = [
        ['Parameter', 'Value', 'Description'],
        ['Algorithm', 'Random Forest', 'Ensemble of Decision Trees'],
        ['n_estimators', '200', 'Number of trees in the forest'],
        ['max_depth', 'None', 'Nodes expanded until pure'],
        ['min_samples_split', '2', 'Min samples to split internal node'],
        ['random_state', '2023', 'Seed for reproducibility'],
        ['class_weight', 'balanced', 'Adjust weights for class imbalance (if any)']
    ]
    
    t = Table(rf_params, colWidths=[2*inch, 1.5*inch, 3*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # 5.4 Evaluation Metrics
    story.append(Paragraph('5.4 Evaluation Metrics', styles['SubsectionHeader']))
    
    metrics_text = """
    Models are evaluated using Stratified K-Fold Cross-Validation (k=5) to ensure robustness.
    """
    story.append(Paragraph(metrics_text, styles['Normal']))
    
    metrics_list = """
    **Classification Metrics (High/Low Prediction):**
    - **Accuracy**: Overall correctness. $\\frac{TP+TN}{Total}$
    - **Precision**: Quality of positive predictions. $\\frac{TP}{TP+FP}$
    - **Recall**: Coverage of actual positives. $\\frac{TP}{TP+FN}$
    - **F1-Score**: Harmonic mean of Precision and Recall. $2 \\cdot \\frac{P \\cdot R}{P + R}$
    
    **Regression Metrics (Grade Prediction):**
    - **Mean Squared Error (MSE)**: Average squared difference between predicted and actual grade.
    - **R-squared ($R^2$)**: Proportion of variance explained by the model.
    """
    story.append(Paragraph(metrics_list, styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 5: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section5_content()