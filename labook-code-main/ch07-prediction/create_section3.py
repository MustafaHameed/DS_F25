#!/usr/bin/env python3
"""
Ch07 SDD Section 3: User Interface
Fills in the User Interface section with input/output specs and dashboard mockups
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_section3_content():
    """Generate Section 3 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section3.pdf'
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
        name='SubsubsectionHeader',
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceAfter=8,
        spaceBefore=8
    ))
    styles.add(ParagraphStyle(
        name='TableCaption',
        fontSize=10,
        fontName='Helvetica-Oblique',
        alignment=1,  # Center
        spaceAfter=5
    ))

    story = []

    # Section 3: User Interface
    story.append(Paragraph('3. User Interface', styles['SectionHeader']))

    # 3.1 System Inputs
    story.append(Paragraph('3.1 System Inputs', styles['SubsectionHeader']))
    input_desc = """
    The system is designed for non-interactive, batch processing and does not have a traditional graphical user interface (GUI) for data input. Instead, it relies on standardized file-based inputs provided by the course instructor or administrator.
    """
    story.append(Paragraph(input_desc, styles['Normal']))

    story.append(Paragraph('3.1.1 Events Data (Events.xlsx)', styles['SubsubsectionHeader']))
    events_input_desc = """
    This Excel file contains the raw Moodle event logs. Each row represents a single student interaction.
    - **Format**: Microsoft Excel (.xlsx)
    - **Sheet Name**: 'events'
    - **Columns**: `user` (string/int), `ts` (datetime string), `action` (string)
    """
    story.append(Paragraph(events_input_desc, styles['Normal']))

    story.append(Paragraph('3.1.2 Results Data (Results.xlsx)', styles['SubsubsectionHeader']))
    results_input_desc = """
    This Excel file contains the final course outcomes for each student, used as the target variable for model training.
    - **Format**: Microsoft Excel (.xlsx)
    - **Sheet Name**: 'results'
    - **Columns**: `user` (string/int), `Final_grade` (float), `Course_outcome` (string: 'High'/'Low')
    """
    story.append(Paragraph(results_input_desc, styles['Normal']))

    # 3.2 System Outputs
    story.append(Paragraph('3.2 System Outputs', styles['SubsectionHeader']))
    output_desc = """
    The system generates several output files that store the results of the prediction pipeline, including engineered features, trained models, and student-level predictions.
    """
    story.append(Paragraph(output_desc, styles['Normal']))

    story.append(Paragraph('3.2.1 Engineered Features (features.pkl)', styles['SubsubsectionHeader']))
    features_output_desc = """
    A Python pickle file containing a pandas DataFrame of the 20+ engineered features for each student, for each prediction week.
    - **Format**: Pickle (.pkl)
    - **Content**: Serialized pandas DataFrame
    - **Usage**: Input for model training and prediction; can be used for further exploratory analysis.
    """
    story.append(Paragraph(features_output_desc, styles['Normal']))

    story.append(Paragraph('3.2.2 Trained Models (trained_model_week_N.joblib)', styles['SubsubsectionHeader']))
    model_output_desc = """
    The trained Random Forest models (one for classification, one for regression) are saved for each prediction week using joblib for efficient storage of scikit-learn objects.
    - **Format**: Joblib (.joblib)
    - **Content**: Serialized scikit-learn pipeline object (Imputer, Scaler, RandomForest model)
    - **Usage**: Re-loading the model for making predictions on new data without retraining.
    """
    story.append(Paragraph(model_output_desc, styles['Normal']))

    story.append(Paragraph('3.2.3 Predictions (predictions_week_N.csv)', styles['SubsubsectionHeader']))
    predictions_output_desc = """
    A CSV file containing the predictions for each student for a given week.
    - **Format**: Comma-Separated Values (.csv)
    - **Content**: Each row contains a student's predicted outcome and probability.
    - **Columns**: `user`, `week`, `predicted_outcome`, `outcome_probability`, `predicted_grade`, `model_version`
    - **Usage**: For instructor review, dashboard visualization, and performance monitoring.
    """
    story.append(Paragraph(predictions_output_desc, styles['Normal']))

    # 3.3 User Interface Mockups (Conceptual)
    story.append(Paragraph('3.3 User Interface Mockups (Conceptual)', styles['SubsectionHeader']))
    mockup_intro = """
    While the core system is non-interactive, the outputs are designed to feed into a potential web-based dashboard for instructors. Below are conceptual mockups for key visualizations.
    """
    story.append(Paragraph(mockup_intro, styles['Normal']))

    story.append(Paragraph('3.3.1 Mockup 1: Student Activity Heatmap', styles['SubsubsectionHeader']))
    mockup1_desc = """
    **Objective**: To visualize the intensity and timing of student engagement over the course duration.
    - **Visualization Type**: Heatmap
    - **X-Axis**: Day of the course (e.g., Day 1 to Day 35)
    - **Y-Axis**: Student ID, sorted by final grade or predicted outcome.
    - **Color Intensity**: Represents the number of actions on a given day (e.g., light blue for low activity, dark blue for high activity).
    - **Interactivity**: Hovering over a cell shows the exact action count for that student on that day. A dropdown filter allows viewing by course week.
    - **Insight**: Helps instructors quickly identify periods of high/low engagement and spot students with unusual activity patterns (e.g., cramming vs. consistent effort).
    """
    story.append(Paragraph(mockup1_desc, styles['Normal']))

    story.append(Paragraph('3.3.2 Mockup 2: Weekly Prediction Timeline', styles['SubsubsectionHeader']))
    mockup2_desc = """
    **Objective**: To track the evolution of a student's predicted success probability over time.
    - **Visualization Type**: Line Chart
    - **X-Axis**: Prediction Week (Week 1 to Week 5)
    - **Y-Axis**: Predicted Probability of 'High' Outcome (0.0 to 1.0)
    - **Controls**: A dropdown menu to select a specific student. The chart displays a line for the selected student, with markers at each week. A horizontal line at 0.5 indicates the decision boundary.
    - **Interactivity**: Clicking on a data point reveals the top 3 features that contributed to that week's prediction (using feature importance).
    - **Insight**: Allows instructors to monitor a student's trajectory and see if interventions are having a positive effect on their predicted outcome.
    """
    story.append(Paragraph(mockup2_desc, styles['Normal']))

    story.append(Paragraph('3.3.3 Mockup 3: Feature Importance Explorer', styles['SubsubsectionHeader']))
    mockup3_desc = """
    **Objective**: To understand which behaviors are most predictive of success at different points in the course.
    - **Visualization Type**: Bar Chart
    - **Y-Axis**: List of all 20+ engineered features (e.g., 'median_session_len', 'entropy_daily_cnts').
    - **X-Axis**: Feature Importance Score (e.g., Gini importance from Random Forest).
    - **Controls**: A dropdown to select the prediction week (1-5). The chart updates to show the feature importance ranking for the model trained that week.
    - **Interactivity**: Clicking on a feature bar displays a short description of what the feature measures and a distribution plot (histogram) showing the values for 'High' vs. 'Low' outcome students.
    - **Insight**: Helps instructors and curriculum designers understand what student behaviors are critical at different stages of the course, informing pedagogical strategies.
    """
    story.append(Paragraph(mockup3_desc, styles['Normal']))

    # 3.4 API Endpoints (Conceptual)
    story.append(Paragraph('3.4 API Endpoints (Conceptual)', styles['SubsectionHeader']))
    api_desc = """
    For integration with other university systems (e.g., a central student dashboard), the prediction results could be exposed via a RESTful API.
    - **`GET /predictions/{course_id}/{user_id}`**: Retrieves the latest prediction for a specific student in a course. Returns a JSON object with `week`, `predicted_outcome`, `probability`, and `timestamp`.
    - **`GET /predictions/{course_id}/week/{week_num}`**: Retrieves all predictions for a given course and week. Returns a list of student prediction objects.
    - **`POST /predict/{course_id}`**: Triggers a new batch prediction run for the specified course. This is an asynchronous call that returns a job ID to check for status.
    """
    story.append(Paragraph(api_desc, styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 3: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section3_content()