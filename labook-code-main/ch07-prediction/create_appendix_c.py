#!/usr/bin/env python3
"""
Ch07 SDD Appendix C: Code Samples
Fills in Appendix C with key code snippets.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, XPreformatted
from reportlab.lib.units import inch

def create_appendix_c_content():
    """Generate Appendix C content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Appendix_C.pdf'
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
    
    # Code Style
    code_style = getSampleStyleSheet()['Code']
    code_style.backColor = colors.whitesmoke
    code_style.borderPadding = 5
    code_style.fontSize = 8
    code_style.fontName = 'Courier'

    story = []

    # Appendix C
    story.append(Paragraph('Appendix C: Code Samples & Pseudocode', styles['AppendixHeader']))
    story.append(Paragraph('This appendix provides reference implementations for the critical algorithms in the pipeline.', styles['Normal']))
    story.append(Spacer(1, 15))

    # 1. Sessionization Logic
    story.append(Paragraph('1. Sessionization Algorithm (Python/Pandas)', styles['SectionHeader']))
    story.append(Paragraph('The following code groups events into sessions based on the 1.5-hour inactivity threshold.', styles['Normal']))
    
    session_code = """
def sessionize_events(events_df, threshold_hours=1.5):
    # Sort by user and timestamp
    events_df = events_df.sort_values(by=['user', 'ts'])
    
    # Calculate time difference between consecutive events
    events_df['ts_diff'] = events_df.groupby('user')['ts'].diff()
    
    # Convert threshold to seconds
    threshold_sec = threshold_hours * 3600
    
    # Identify session breaks (gap > threshold)
    events_df['is_new_session'] = (events_df['ts_diff'].dt.total_seconds() > threshold_sec) | \\
                                  (events_df['ts_diff'].isnull())
    
    # Assign session IDs (cumulative sum of breaks)
    events_df['session_id'] = events_df.groupby('user')['is_new_session'].cumsum()
    
    return events_df
"""
    story.append(XPreformatted(session_code, code_style))

    # 2. Entropy Calculation
    story.append(Paragraph('2. Entropy Feature Computation', styles['SectionHeader']))
    story.append(Paragraph('Calculates Shannon entropy for a distribution of values (e.g., sessions per day).', styles['Normal']))

    entropy_code = """
import numpy as np
from scipy.stats import entropy

def calculate_entropy(data_series):
    # Get counts of each unique value
    value_counts = data_series.value_counts()
    
    # Calculate probability distribution
    probabilities = value_counts / len(data_series)
    
    # Compute Shannon entropy (base 2)
    return entropy(probabilities, base=2)
"""
    story.append(XPreformatted(entropy_code, code_style))

    # 3. Model Training Pipeline
    story.append(Paragraph('3. Model Training Pipeline', styles['SectionHeader']))
    story.append(Paragraph('Scikit-learn pipeline definition for the Random Forest model.', styles['Normal']))
    
    train_code = """
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

def build_training_pipeline():
    # Define the pipeline steps
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),  # Handle missing data
        ('scaler', StandardScaler()),                 # Normalize features
        ('rf', RandomForestClassifier(                # Classification Model
            n_estimators=200,
            criterion='gini',
            class_weight='balanced',
            random_state=2023
        ))
    ])
    
    return pipeline
"""
    story.append(XPreformatted(train_code, code_style))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Appendix C: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_appendix_c_content()