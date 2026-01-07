#!/usr/bin/env python3
"""
Ch07 SDD Section 1: Application Architecture
Fills in the Application Architecture section with detailed content
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def create_section1_content():
    """Generate Section 1 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section1.pdf'
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
        name='CodeBlock',
        fontSize=10,
        fontName='Courier',
        backgroundColor=colors.lightgrey,
        borderPadding=5,
        spaceAfter=10
    ))

    story = []

    # Section 1: Application Architecture
    story.append(Paragraph('1. Application Architecture', styles['SectionHeader']))

    # 1.1 System Overview
    story.append(Paragraph('1.1 System Overview', styles['SubsectionHeader']))
    overview = """
    The Learning Analytics Prediction System is a comprehensive data processing and machine learning pipeline designed to transform raw Moodle Learning Management System (LMS) event logs into predictive models for student success. The system ingests student interaction data, processes it through multiple analytical stages, and outputs trained models capable of forecasting course outcomes and final grades.

    The system operates on a batch processing model where historical course data is processed to train predictive models that can be applied to ongoing courses. The core workflow consists of six main components: Data Ingestion, Preprocessing, Sessionization, Feature Engineering, Model Training, and Prediction & Evaluation.

    Key system characteristics:
    • Input: Excel files containing student event logs and grade outcomes
    • Processing: Python-based pipeline using pandas, scikit-learn, and custom algorithms
    • Output: Trained Random Forest models, feature datasets, and evaluation metrics
    • Scale: Designed for single-course analysis (200-400 students, 10,000+ events)
    • Prediction Horizon: Rolling window predictions from weeks 1-5 of course activity
    """
    story.append(Paragraph(overview, styles['Normal']))

    # 1.2 Architecture Diagrams
    story.append(Paragraph('1.2 Architecture Diagrams', styles['SubsectionHeader']))

    story.append(Paragraph('1.2.1 System Context Diagram', styles['SubsectionHeader']))
    context_desc = """
    The system context diagram (Figure 1.1) shows the system's relationship with external entities:

    External Entities:
    • Moodle LMS: Provides raw event logs (Events.xlsx) and grade outcomes (Results.xlsx)
    • Instructor/Dashboard User: Consumes predictions, feature importance, and evaluation metrics
    • File System: Stores intermediate data (preprocessed_data/), models (models/), and outputs

    Data Flows:
    • Input: Excel files → System → Processed datasets and trained models
    • Output: CSV exports, pickle files, joblib models, PDF reports
    """
    story.append(Paragraph(context_desc, styles['Normal']))

    story.append(Paragraph('1.2.2 Component Diagram', styles['SubsectionHeader']))
    component_desc = """
    The component diagram (Figure 1.2) illustrates the six core system components and their interactions:

    1. Data Ingestion Component
       • Reads Events.xlsx and Results.xlsx using pandas
       • Validates file formats and required columns
       • Handles timestamp parsing and data type conversion

    2. Preprocessing Component
       • Normalizes timestamp columns across different formats
       • Computes course weeks using Monday-based week boundaries
       • Creates binary course outcome variable (High/Low) via median split

    3. Sessionization Component
       • Groups events into sessions using 1.5-hour inactivity threshold
       • Computes session start/end times and durations
       • Generates session-level aggregations per user

    4. Feature Engineering Component
       • Computes 20+ behavioral features from sessionized data
       • Includes action counts, entropy measures, session statistics, temporal patterns
       • Handles missing data imputation and feature scaling

    5. Model Training Component
       • Trains separate models for each prediction week (1-5)
       • Uses Random Forest for both classification (course outcome) and regression (final grade)
       • Implements cross-validation and hyperparameter tuning

    6. Prediction & Evaluation Component
       • Generates predictions on held-out test sets
       • Computes comprehensive evaluation metrics (Accuracy, F1, RMSE, R²)
       • Exports model artifacts and performance reports
    """
    story.append(Paragraph(component_desc, styles['Normal']))

    story.append(Paragraph('1.2.3 Data Flow Diagram', styles['SubsectionHeader']))
    dfd_desc = """
    The Data Flow Diagram (DFD) (Figure 1.3) shows the transformation of data through the system:

    Level 0 Processes:
    • P1: Data Ingestion (Excel → DataFrames)
    • P2: Preprocessing (Raw data → Cleaned events + results)
    • P3: Sessionization (Events → Session groups)
    • P4: Feature Engineering (Sessions → Feature vectors)
    • P5: Model Training (Features + labels → Trained models)
    • P6: Evaluation (Predictions → Metrics + reports)

    Data Stores:
    • DS1: Raw Events (Events.xlsx)
    • DS2: Grade Outcomes (Results.xlsx)
    • DS3: Processed Events (events.pkl)
    • DS4: Session Data (events_with_sessions.pkl)
    • DS5: Feature Matrices (computed per week)
    • DS6: Trained Models (model_week_*.joblib)

    Key Data Transformations:
    • Events (user, timestamp, action) → Sessions (session_id, duration, action_counts)
    • Sessions → Features (entropy, session_stats, temporal_patterns)
    • Features + Labels → Predictions (outcome_probabilities, grade_estimates)
    """
    story.append(Paragraph(dfd_desc, styles['Normal']))

    # 1.3 Technology Stack
    story.append(Paragraph('1.3 Technology Stack', styles['SubsectionHeader']))

    tech_stack = """
    Core Technologies:
    • Programming Language: Python 3.12.12
    • Data Processing: pandas 2.3.2, numpy 1.26.4
    • Machine Learning: scikit-learn 1.7.2
    • Statistical Analysis: scipy 1.16.3, statsmodels 0.14.5
    • Visualization: matplotlib 3.10.6, seaborn 0.13.2
    • PDF Generation: reportlab 4.4.4
    • Model Serialization: joblib 1.4.2
    • Excel Processing: openpyxl 3.1.5

    Development Environment:
    • IDE: VS Code with Python extension
    • Version Control: Git (GitHub repository)
    • Package Management: Conda environment
    • Documentation: Jupyter notebooks, PDF reports

    System Dependencies:
    • Operating System: Windows 10/11 (primary), Linux/MacOS (compatible)
    • Memory Requirements: 4GB RAM minimum, 8GB recommended
    • Storage: 500MB for code + data, additional space for models
    • Python Environment: Conda base environment with scientific computing stack
    """
    story.append(Paragraph(tech_stack, styles['Normal']))

    # 1.4 System Constraints
    story.append(Paragraph('1.4 System Constraints', styles['SubsectionHeader']))

    constraints = """
    Performance Constraints:
    • Maximum Dataset Size: 50,000 events (single course limit)
    • Processing Time: <30 minutes for full pipeline execution
    • Memory Usage: <2GB RAM during normal operation
    • Model Training Time: <5 minutes per week (Random Forest with 200 trees)

    Scalability Limitations:
    • Single Course Focus: Designed for individual course analysis, not multi-course aggregation
    • Batch Processing: Not optimized for real-time predictions
    • Feature Count: Limited to ~25 features to maintain interpretability
    • Model Complexity: Random Forest only (no deep learning due to interpretability requirements)

    Data Quality Assumptions:
    • Complete Event Logs: Assumes comprehensive LMS tracking (no missing critical events)
    • Timestamp Accuracy: Requires reliable server-side timestamps
    • Grade Data Availability: Needs final grade outcomes for supervised learning
    • User Consistency: Assumes stable user IDs across course duration

    Operational Constraints:
    • Manual Execution: Requires user initiation of pipeline (no automated scheduling)
    • File Format Dependency: Excel-based input (not API-based ingestion)
    • Environment Consistency: Requires specific Python package versions
    • Output Format Limitations: CSV/pickle exports (no database integration)
    """
    story.append(Paragraph(constraints, styles['Normal']))

    # 1.5 Component Interfaces
    story.append(Paragraph('1.5 Component Interfaces', styles['SubsectionHeader']))

    interfaces = """
    Data Ingestion Interface:
    • Input: File paths to Events.xlsx, Results.xlsx
    • Output: pandas DataFrames (events_df, results_df)
    • Error Handling: File not found, invalid format, missing columns

    Preprocessing Interface:
    • Input: Raw events DataFrame, results DataFrame
    • Output: Processed events with course_week, binary outcomes
    • Validation: Timestamp format checking, data completeness

    Sessionization Interface:
    • Input: Processed events DataFrame
    • Output: events_with_sessions DataFrame with session_id, session_len
    • Parameters: inactivity_threshold (default: 1.5 hours)

    Feature Engineering Interface:
    • Input: events_with_sessions DataFrame, week_k (prediction week)
    • Output: Feature matrix (users × features), feature names list
    • Features: 20+ computed metrics (action counts, entropy, session stats)

    Model Training Interface:
    • Input: Feature matrix, target vector, model type (classification/regression)
    • Output: Trained pipeline (imputer + scaler + estimator), evaluation metrics
    • Parameters: test_size=0.2, random_state=2023, n_estimators=200

    Prediction Interface:
    • Input: Trained model, feature matrix for new data
    • Output: Predictions, probabilities (classification), confidence intervals
    • Error Handling: Feature mismatch, missing data imputation
    """
    story.append(Paragraph(interfaces, styles['Normal']))

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 1: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section1_content()