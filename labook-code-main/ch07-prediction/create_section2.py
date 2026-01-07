#!/usr/bin/env python3
"""
Ch07 SDD Section 2: Data Model Schema
Fills in the Data Model Schema section with ERD and table definitions
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_section2_content():
    """Generate Section 2 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section2.pdf'
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
        name='TableCaption',
        fontSize=10,
        fontName='Helvetica-Oblique',
        alignment=1,  # Center
        spaceAfter=5
    ))

    story = []

    # Section 2: Data Model Schema
    story.append(Paragraph('2. Data Model Schema', styles['SectionHeader']))

    # 2.1 Entity-Relationship Diagram
    story.append(Paragraph('2.1 Entity-Relationship Diagram', styles['SubsectionHeader']))
    erd_desc = """
    The Entity-Relationship Diagram (ERD) for the Learning Analytics Prediction System consists of five primary entities that represent the complete data transformation pipeline from raw events to predictive models. The ERD follows a star schema design with Events as the central fact table and supporting dimension tables for Sessions, Features, Results, and Predictions.

    Entity Overview:
    • Events (Central Fact Table): Raw student interaction data from Moodle LMS
    • Sessions (Derived Dimension): User session groupings based on activity patterns
    • Features (Computed Dimension): Engineered predictive features per user per week
    • Results (Outcome Dimension): Student performance outcomes and grades
    • Predictions (Output Dimension): Model predictions and evaluation metrics

    Key Relationships:
    • Events → Sessions: One-to-many (each event belongs to one session)
    • Events → Features: Many-to-one (events aggregate to user-level features)
    • Results → Features: One-to-one (each student has feature vector and outcome)
    • Features → Predictions: One-to-many (features used for multiple week predictions)
    """
    story.append(Paragraph(erd_desc, styles['Normal']))

    # 2.2 Table Definitions
    story.append(Paragraph('2.2 Table Definitions', styles['SubsectionHeader']))

    # Events Table
    story.append(Paragraph('2.2.1 Events Table', styles['SubsectionHeader']))
    events_desc = """
    The Events table stores raw student interaction data extracted from Moodle LMS event logs. This is the primary input table containing all user actions throughout the course duration.
    """
    story.append(Paragraph(events_desc, styles['Normal']))

    # Events table schema
    events_schema = [
        ['Column Name', 'Data Type', 'Description', 'Constraints', 'Example'],
        ['user', 'string/int', 'Unique student identifier', 'Required, Not Null', '12345'],
        ['ts', 'datetime64[ns]', 'Event timestamp (server time)', 'Required, Not Null', '2023-09-01 14:30:25'],
        ['week', 'int', 'Course week number (1-5)', 'Required, 1-5', '2'],
        ['action', 'string', 'Type of student action', 'Required, Not Null', 'view_forum'],
        ['session_id', 'string', 'Session identifier', 'Optional, Derived', '12345_session_1'],
        ['session_len', 'float', 'Session duration in seconds', 'Optional, Derived', '1847.5'],
        ['ts_diff', 'timedelta', 'Time since previous event', 'Optional, Derived', '00:05:23'],
        ['ts_diff_hours', 'float', 'Time difference in hours', 'Optional, Derived', '0.089']
    ]

    events_table = Table(events_schema, colWidths=[1.5*inch, 1*inch, 2.5*inch, 1.2*inch, 1.2*inch])
    events_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(events_table)
    story.append(Spacer(1, 10))

    # Sessions Table
    story.append(Paragraph('2.2.2 Sessions Table', styles['SubsectionHeader']))
    sessions_desc = """
    The Sessions table contains aggregated session-level data derived from the Events table through the sessionization process. Sessions are defined by 1.5-hour inactivity gaps between consecutive events.
    """
    story.append(Paragraph(sessions_desc, styles['Normal']))

    sessions_schema = [
        ['Column Name', 'Data Type', 'Description', 'Constraints', 'Example'],
        ['session_id', 'string', 'Unique session identifier', 'Primary Key', '12345_session_1'],
        ['user', 'string/int', 'Student identifier', 'Foreign Key → Events.user', '12345'],
        ['session_start', 'datetime64[ns]', 'Session start timestamp', 'Required', '2023-09-01 14:30:25'],
        ['session_end', 'datetime64[ns]', 'Session end timestamp', 'Required', '2023-09-01 16:01:12'],
        ['session_len', 'float', 'Session duration (seconds)', 'Required, >0', '1847.5'],
        ['event_count', 'int', 'Number of events in session', 'Required, >0', '23'],
        ['action_types', 'list', 'Unique actions in session', 'Optional', "['view_forum', 'post_reply']"]
    ]

    sessions_table = Table(sessions_schema, colWidths=[1.5*inch, 1*inch, 2.5*inch, 1.2*inch, 1.2*inch])
    sessions_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(sessions_table)
    story.append(Spacer(1, 10))

    # Features Table
    story.append(Paragraph('2.2.3 Features Table', styles['SubsectionHeader']))
    features_desc = """
    The Features table contains 20+ engineered predictive features computed for each student up to a specific prediction week. Features are derived from session patterns, activity distributions, and temporal behaviors.
    """
    story.append(Paragraph(features_desc, styles['Normal']))

    features_schema = [
        ['Column Name', 'Data Type', 'Description', 'Range/Units', 'Business Meaning'],
        ['user', 'string/int', 'Student identifier', 'N/A', 'Primary Key'],
        ['action_cnt_*', 'int', 'Count of specific actions', '0-500', 'Activity frequency by type'],
        ['avg_actions_per_day', 'float', 'Average daily actions', '0-100', 'Activity intensity'],
        ['entropy_daily_cnts', 'float', 'Daily activity entropy', '0-log2(n)', 'Activity pattern consistency'],
        ['session_cnt', 'int', 'Total sessions', '0-50', 'Learning session frequency'],
        ['median_session_len', 'float', 'Median session duration', '0-7200 sec', 'Typical session length'],
        ['entropy_session_len', 'float', 'Session length entropy', '0-log2(n)', 'Session duration variability'],
        ['active_days_cnt', 'int', 'Days with activity', '0-35', 'Engagement breadth'],
        ['avg_gap_between_active_days', 'float', 'Mean gap between active days', '0-35 days', 'Engagement consistency']
    ]

    features_table = Table(features_schema, colWidths=[1.8*inch, 1*inch, 2.2*inch, 1.2*inch, 1.5*inch])
    features_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(features_table)
    story.append(Spacer(1, 10))

    # Results Table
    story.append(Paragraph('2.2.4 Results Table', styles['SubsectionHeader']))
    results_desc = """
    The Results table contains student performance outcomes used as target variables for supervised learning. Includes both continuous final grades and binary course success indicators.
    """
    story.append(Paragraph(results_desc, styles['Normal']))

    results_schema = [
        ['Column Name', 'Data Type', 'Description', 'Constraints', 'Example'],
        ['user', 'string/int', 'Student identifier', 'Primary Key', '12345'],
        ['Final_grade', 'float', 'Final course grade (numeric)', '0-100', '85.7'],
        ['Course_outcome', 'string', 'Binary success indicator', 'High/Low', 'High'],
        ['grade_percentile', 'float', 'Grade percentile rank', '0-100', '78.5'],
        ['outcome_confidence', 'float', 'Outcome determination confidence', '0-1', '0.95']
    ]

    results_table = Table(results_schema, colWidths=[1.5*inch, 1*inch, 2.5*inch, 1.2*inch, 1.2*inch])
    results_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(results_table)
    story.append(Spacer(1, 10))

    # Predictions Table
    story.append(Paragraph('2.2.5 Predictions Table', styles['SubsectionHeader']))
    predictions_desc = """
    The Predictions table stores model outputs including predicted outcomes, probabilities, and evaluation metrics for each prediction week and student.
    """
    story.append(Paragraph(predictions_desc, styles['Normal']))

    predictions_schema = [
        ['Column Name', 'Data Type', 'Description', 'Constraints', 'Example'],
        ['user', 'string/int', 'Student identifier', 'Foreign Key', '12345'],
        ['week', 'int', 'Prediction week', '1-5', '3'],
        ['predicted_outcome', 'string', 'Predicted course outcome', 'High/Low', 'High'],
        ['outcome_probability', 'float', 'Prediction confidence', '0-1', '0.78'],
        ['predicted_grade', 'float', 'Predicted final grade', '0-100', '82.3'],
        ['model_version', 'string', 'Model identifier', 'Required', 'rf_class_week_3_v1'],
        ['feature_count', 'int', 'Features used', '20-25', '22'],
        ['prediction_timestamp', 'datetime64[ns]', 'When prediction made', 'Auto', '2023-12-01 10:30:00']
    ]

    predictions_table = Table(predictions_schema, colWidths=[1.5*inch, 1*inch, 2.5*inch, 1.2*inch, 1.2*inch])
    predictions_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(predictions_table)
    story.append(Spacer(1, 10))

    # 2.3 Data Relationships
    story.append(Paragraph('2.3 Data Relationships', styles['SubsectionHeader']))

    relationships = """
    Primary Key Relationships:
    • Events.user → Results.user (1:1) - Each student has one outcome record
    • Events.user → Features.user (1:1) - Each student has one feature vector per week
    • Features.user + Features.week → Predictions.user + Predictions.week (1:1) - Each student-week has one prediction

    Foreign Key Relationships:
    • Events.session_id → Sessions.session_id (Many:1) - Multiple events belong to one session
    • Sessions.user → Events.user (Many:1) - Sessions are grouped by user
    • Predictions.model_version → Model Registry (Many:1) - Predictions reference specific model versions

    Data Flow Dependencies:
    1. Events must exist before Sessions can be created
    2. Sessions must exist before Features can be computed
    3. Results must exist for supervised model training
    4. Features + Results enable Predictions generation

    Cardinality Summary:
    • Students: 200-400 per course
    • Events per student: 50-200 (total: 10,000-80,000 events)
    • Sessions per student: 5-30
    • Features per student per week: 20-25
    • Predictions per student: 5 (one per week)
    """
    story.append(Paragraph(relationships, styles['Normal']))

    # 2.4 Data Validation Rules
    story.append(Paragraph('2.4 Data Validation Rules', styles['SubsectionHeader']))

    validation = """
    Events Table Validation:
    • user: Must be non-null, consistent format across course
    • ts: Must be valid datetime, within course start/end dates
    • action: Must be from predefined Moodle action types
    • week: Must be integer 1-5, consistent with course timeline

    Sessions Table Validation:
    • session_len: Must be > 0 and < 24 hours (reasonable session duration)
    • session_start < session_end: Temporal consistency
    • event_count: Must be >= 1

    Features Table Validation:
    • All count features: Must be >= 0
    • Entropy features: Must be >= 0 and <= log2(max_possible_bins)
    • avg_gap_between_active_days: Must be >= 0 and <= course_length_days

    Results Table Validation:
    • Final_grade: Must be 0-100 (or equivalent scale)
    • Course_outcome: Must be exactly 'High' or 'Low'

    Predictions Table Validation:
    • outcome_probability: Must be 0.0-1.0
    • predicted_grade: Must be 0-100 (or match input scale)
    • week: Must match training week range
    """
    story.append(Paragraph(validation, styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 2: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section2_content()