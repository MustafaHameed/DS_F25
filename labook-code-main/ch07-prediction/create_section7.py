#!/usr/bin/env python3
"""
Ch07 SDD Section 7: Deployment & Operations
Fills in the Deployment & Operations section with pipeline details, versioning, and maintenance procedures.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch

def create_section7_content():
    """Generate Section 7 content for SDD"""

    # Document setup
    pdf_path = 'Ch07_SDD_Section7.pdf'
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

    # Section 7: Deployment & Operations
    story.append(Paragraph('7. Deployment & Operations', styles['SectionHeader']))
    
    intro = """
    This section describes how the Learning Analytics Prediction System is deployed, operated, and maintained in a production environment. Since the system operates as a batch processing utility rather than a real-time service, the operational focus is on the weekly execution pipeline.
    """
    story.append(Paragraph(intro, styles['Normal']))

    # 7.1 Batch Prediction Pipeline
    story.append(Paragraph('7.1 Batch Prediction Pipeline', styles['SubsectionHeader']))
    
    pipeline_text = """
    The core operational process is the **Weekly Prediction Cycle**, which runs at the end of every course week (e.g., Sunday night).
    """
    story.append(Paragraph(pipeline_text, styles['Normal']))
    
    pipeline_steps = ListFlowable(
        [
            ListItem(Paragraph("**Step 1: Data Ingestion:** New Moodle event logs for the completed week are exported and appended to `Events.xlsx`.", styles['Normal'])),
            ListItem(Paragraph("**Step 2: Preprocessing & Sessionization:** The system re-processes the cumulative event log to update session attributes and handle any late-arriving data.", styles['Normal'])),
            ListItem(Paragraph("**Step 3: Feature Engineering:** Features are re-computed for all students up to the current week ($W_{current}$).", styles['Normal'])),
            ListItem(Paragraph("**Step 4: Model Retraining:** The Random Forest model is retrained using data from all previous years plus the current semester up to $W_{current}$.", styles['Normal'])),
            ListItem(Paragraph("**Step 5: Prediction Generation:** The new model generates predictions for the upcoming week ($W_{next}$) for all active students.", styles['Normal'])),
            ListItem(Paragraph("**Step 6: Output Delivery:** Predictions are exported to `predictions_week_N.csv` and dashboards are updated.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(pipeline_steps)

    # 7.2 Model Versioning Strategy
    story.append(Paragraph('7.2 Model Versioning Strategy', styles['SubsectionHeader']))
    
    versioning_text = """
    To ensure reproducibility and accountability, comprehensive model versioning is implemented. Each prediction record includes the specific model version used to generate it.
    """
    story.append(Paragraph(versioning_text, styles['Normal']))
    
    versioning_list = ListFlowable(
        [
            ListItem(Paragraph("**Naming Convention:** Models are saved with the format `model_{type}_week_{w}_v{major}.{minor}.joblib` (e.g., `model_class_week_3_v1.0.joblib`).", styles['Normal'])),
            ListItem(Paragraph("**Artifact Tracking:** Alongside the serialized model, a `model_metadata.json` file is saved, recording the hyperparameter configuration, training data hash, and performance metrics (F1/R2) at training time.", styles['Normal'])),
            ListItem(Paragraph("**Changelog:** Any changes to the feature engineering code trigger a major version increment (v1.0 -> v2.0), while routine weekly retraining triggers a minor version increment (v1.0 -> v1.1).", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(versioning_list)

    # 7.3 Monitoring & Alerting
    story.append(Paragraph('7.3 Operational Monitoring', styles['SubsectionHeader']))
    
    monitor_text = """
    System health is monitored based on both computational success and model performance metrics.
    """
    story.append(Paragraph(monitor_text, styles['Normal']))
    
    monitor_list = ListFlowable(
        [
            ListItem(Paragraph("**Performance Drift:** If the Cross-Validation F1-score drops below 0.65 (or another defined threshold) during retraining, an alert is triggered for the data scientist to investigate potential data quality issues or concept drift.", styles['Normal'])),
            ListItem(Paragraph('**Data Quality Checks:** The pipeline validates input data volume. If the number of events for the current week is < 10% of the average, a "Missing Data" alert is raised.', styles['Normal'])),
            ListItem(Paragraph("**Execution Time:** If the batch processing time exceeds 4 hours, a performance warning is logged to indicate potential scalability bottlenecks.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(monitor_list)

    # 7.4 Error Handling & Maintenance
    story.append(Paragraph('7.4 Error Handling & Maintenance', styles['SubsectionHeader']))
    
    maint_list = ListFlowable(
        [
            ListItem(Paragraph("**Missing Feautures:** If a student has zero activity for a week, the system handles missing feature values using 0-imputation (for counts) or mean-imputation (for temporal stats), flagged by an `is_imputed` column.", styles['Normal'])),
            ListItem(Paragraph("**Corrupt Input:** If `Events.xlsx` is unreadable or malformed, the pipeline halts immediately (Fail Fast) and notifies the administrator, preventing the generation of garbage predictions.", styles['Normal'])),
            ListItem(Paragraph("**Archival:** At the end of the semester, execution logs, intermediate feature checkpoints, and model artifacts are zipped and archived to cold storage (`/archive/Semester_Year/`) for 5 years to comply with academic record retention policies.", styles['Normal'])),
        ],
        bulletType='bullet',
        start='bulletchar'
    )
    story.append(maint_list)

    # Build PDF
    try:
        doc.build(story)
        print(f'Successfully created Section 7: {pdf_path}')
        print(f'File size: {os.path.getsize(pdf_path)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_section7_content()