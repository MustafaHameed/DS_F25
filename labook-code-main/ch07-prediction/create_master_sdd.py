#!/usr/bin/env python3
"""
Ch07 Master SDD Generator
Generates the complete Software Design Document (SDD) for the Learning Analytics Prediction System.
Integrates all sections, diagrams, and appendices into a single professional PDF.
"""

import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
                                PageBreak, Image, ListFlowable, ListItem, KeepTogether)
from reportlab.lib.units import inch

# --- Configuration ---
PDF_PATH = 'Ch07_SDD_Complete.pdf'
DIAGRAMS_DIR = 'diagrams'

def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    page_num = canvas.getPageNumber()
    text = "Ch07 Learning Analytics Prediction System - Software Design Document"
    canvas.drawString(inch, 10.5 * inch, text)
    canvas.drawRightString(7.5 * inch, 0.75 * inch, f"Page {page_num}")
    canvas.restoreState()

def create_master_sdd():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=0.8*inch,
        leftMargin=0.8*inch,
        topMargin=1.0*inch,  # Space for header
        bottomMargin=1.0*inch # Space for footer
    )

    # --- Styles ---
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_title = ParagraphStyle('Title', parent=styles['Title'], fontSize=24, spaceAfter=20)
    style_subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, spaceAfter=50)
    style_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, spaceBefore=20, spaceAfter=10, keepWithNext=True)
    style_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, spaceBefore=15, spaceAfter=8, keepWithNext=True)
    style_h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=12, spaceBefore=10, spaceAfter=6, keepWithNext=True)
    style_normal = ParagraphStyle('Normal_Justified', parent=styles['Normal'], alignment=TA_JUSTIFY, spaceAfter=8)
    style_code = ParagraphStyle('Code', parent=styles['Code'], backColor=colors.whitesmoke, borderPadding=5, fontSize=9)
    
    story = []

    # =========================================================================
    # 0. Front Matter
    # =========================================================================
    
    # Cover Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Software Design Document", style_title))
    story.append(Paragraph("Learning Analytics Prediction System (Ch07)", style_subtitle))
    story.append(Spacer(1, 1*inch))
    
    data_table = [
        ['Author:', 'Mustafa Hameed'],
        ['Date:', datetime.date.today().strftime('%B %d, %Y')],
        ['Version:', '1.0'],
        ['Repository:', 'DS_F25 / labook-code-main']
    ]
    t_info = Table(data_table, colWidths=[2*inch, 3*inch])
    t_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_info)
    story.append(PageBreak())

    # Abstract
    story.append(Paragraph("Abstract", style_h1))
    abstract_text = """
    This Software Design Document (SDD) details the architecture and implementation of the "Learning Analytics Prediction System" (Ch07). 
    The system is a machine learning pipeline designed to predict student academic performance in online courses based on their interaction logs 
    from the Moodle Learning Management System (LMS). By analyzing behavioral patterns such as study session regularity (entropy) and 
    engagement intensity, the system identifies at-risk students week-by-week, enabling timely instructor interventions.
    """
    story.append(Paragraph(abstract_text, style_normal))
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("Table of Contents", style_h1))
    story.append(Paragraph("1. Application Architecture", style_normal))
    story.append(Paragraph("2. Data Model Schema", style_normal))
    story.append(Paragraph("3. User Interface", style_normal))
    story.append(Paragraph("4. Design Decisions & Rationale", style_normal))
    story.append(Paragraph("5. Algorithm & Methodology", style_normal))
    story.append(Paragraph("6. Security & Data Privacy", style_normal))
    story.append(Paragraph("7. Deployment & Operations", style_normal))
    story.append(Paragraph("8. Testing Strategy", style_normal))
    story.append(Paragraph("Appendices A-D", style_normal))
    story.append(PageBreak())

    # =========================================================================
    # 1. Application Architecture
    # =========================================================================
    story.append(Paragraph("1. Application Architecture", style_h1))
    story.append(Paragraph("The system follows a modular pipeline architecture designed for batch processing of student data.", style_normal))
    
    # Context Diagram
    context_img_path = os.path.join(DIAGRAMS_DIR, '01_system_context.png')
    if os.path.exists(context_img_path):
        story.append(Image(context_img_path, width=6*inch, height=2.5*inch))
        story.append(Paragraph("<i>Figure 1: System Context Diagram</i>", styles['Normal']))
        story.append(Spacer(1, 10))

    story.append(Paragraph("1.1 Core Components", style_h2))
    
    # Component Diagram
    comp_img_path = os.path.join(DIAGRAMS_DIR, '02_component_diagram.png')
    if os.path.exists(comp_img_path):
        story.append(Image(comp_img_path, width=4*inch, height=5*inch))
        story.append(Paragraph("<i>Figure 2: Component Diagram</i>", styles['Normal']))

    story.append(Paragraph("The system consists of six primary components:", style_normal))
    comp_list = ListFlowable([
        ListItem(Paragraph("<b>1. Data Ingestion:</b> Parsers for reading raw `Events.xlsx` and target `Results.xlsx`.", style_normal)),
        ListItem(Paragraph("<b>2. Preprocessing:</b> Timezone normalization and data cleaning.", style_normal)),
        ListItem(Paragraph("<b>3. Sessionization:</b> Algorithms to group raw clicks into study sessions (1.5h threshold).", style_normal)),
        ListItem(Paragraph("<b>4. Feature Engineering:</b> Computation of 20+ predictive features per student/week.", style_normal)),
        ListItem(Paragraph("<b>5. Model Training:</b> Random Forest classifiers/regressors trained on historical weeks.", style_normal)),
        ListItem(Paragraph("<b>6. Prediction Engine:</b> Applies models to generate risk scores for current students.", style_normal)),
    ], bulletType='bullet', start='bulletchar')
    story.append(comp_list)

    # =========================================================================
    # 2. Data Model Schema
    # =========================================================================
    story.append(Paragraph("2. Data Model Schema", style_h1))
    
    # ERD
    erd_img_path = os.path.join(DIAGRAMS_DIR, '04_erd.png')
    if os.path.exists(erd_img_path):
        story.append(Image(erd_img_path, width=4*inch, height=4*inch))
        story.append(Paragraph("<i>Figure 3: Entity-Relationship Diagram</i>", styles['Normal']))

    story.append(Paragraph("2.1 Entity Definitions", style_h2))
    
    # Events Table Definition (Reusing logic from Section 2)
    events_schema = [
        ['Column', 'Type', 'Description'],
        ['user', 'string', 'Unique Student ID'],
        ['ts', 'datetime', 'Interaction Timestamp'],
        ['action', 'string', 'Interaction Type (view, post)'],
        ['week', 'int', 'Course Week (1-5)']
    ]
    t_events = Table(events_schema, colWidths=[1.5*inch, 1.5*inch, 3*inch])
    t_events.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(Paragraph("<b>Events Table (Fact)</b>", style_h3))
    story.append(t_events)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. User Interface
    # =========================================================================
    story.append(Paragraph("3. User Interface", style_h1))
    story.append(Paragraph("3.1 Input/Output Interfaces", style_h2))
    story.append(Paragraph("The system is primarily a backend service processing file-based inputs:", style_normal))
    
    io_list = ListFlowable([
        ListItem(Paragraph("<b>Inputs:</b> Excel files (`Events.xlsx`, `Results.xlsx`) provided by course admins.", style_normal)),
        ListItem(Paragraph("<b>Outputs:</b> CSV files (`predictions.csv`) for dashboard consumption.", style_normal)),
    ], bulletType='bullet')
    story.append(io_list)

    story.append(Paragraph("3.2 Conceptual Dashboard", style_h2))
    story.append(Paragraph("The prediction results feed into an Instructor Dashboard featuring:", style_normal))
    dash_list = ListFlowable([
        ListItem(Paragraph("<b>Risk Heatmap:</b> Visualizing student risk levels across weeks.", style_normal)),
        ListItem(Paragraph("<b>Detail View:</b> Drill-down into a student's specific feature drivers (e.g., 'Low Session Consistency').", style_normal)),
    ], bulletType='bullet')
    story.append(dash_list)

    # =========================================================================
    # 4. Design Decisions
    # =========================================================================
    story.append(Paragraph("4. Design Decisions", style_h1))
    story.append(Paragraph("<b>Sessionization Threshold (1.5h):</b> Chosen based on educational psychology research indicating standard study block limits.", style_normal))
    story.append(Paragraph("<b>Random Forest Model:</b> Selected for its ability to handle non-linear relationships and high-order interactions in behavioral data better than linear models.", style_normal))
    story.append(Paragraph("<b>Entropy Features:</b> Used explicitly to capture the 'consistency' of student habits, distinguishing between crammers (low entropy) and regular studiers (high entropy).", style_normal))

    # =========================================================================
    # 5. Algorithm & Methodology
    # =========================================================================
    story.append(Paragraph("5. Algorithm & Methodology", style_h1))
    
    # Feature Pipeline Diagram
    pipe_img_path = os.path.join(DIAGRAMS_DIR, '05_feature_pipeline.png')
    if os.path.exists(pipe_img_path):
        story.append(Image(pipe_img_path, width=4*inch, height=5*inch))
        story.append(Paragraph("<i>Figure 4: Feature Engineering Pipeline</i>", styles['Normal']))

    story.append(Paragraph("5.1 Feature Engineering", style_h2))
    story.append(Paragraph("Key features include:", style_normal))
    feat_list = ListFlowable([
        ListItem(Paragraph("<b>Activity Counts:</b> Total actions, actions per type.", style_normal)),
        ListItem(Paragraph("<b>Temporal:</b> Median session length, average gap between active days.", style_normal)),
        ListItem(Paragraph("<b>Entropy:</b> Shannon entropy of daily activity counts.", style_normal)),
    ], bulletType='bullet')
    story.append(feat_list)

    # DFD Diagram
    story.append(Paragraph("5.2 Data Flow Logic", style_h2))
    dfd_img_path = os.path.join(DIAGRAMS_DIR, '03_data_flow.png')
    if os.path.exists(dfd_img_path):
        story.append(Image(dfd_img_path, width=6*inch, height=2.5*inch))
        story.append(Paragraph("<i>Figure 5: Data Flow Diagram (Level 1)</i>", styles['Normal']))

    # =========================================================================
    # 6. Security & Data Privacy
    # =========================================================================
    story.append(Paragraph("6. Security & Data Privacy", style_h1))
    story.append(Paragraph("The system is FERPA-compliant. All internal processing uses pseudonymized User IDs. Mapping tables are stored offline. Data access is restricted to authorized instructors only.", style_normal))

    # =========================================================================
    # 7. Deployment & Operations
    # =========================================================================
    story.append(Paragraph("7. Deployment & Operations", style_h1))
    story.append(Paragraph("The system operates on a weekly batch cycle (Sunday nights). Models are versioned (e.g., v1.0, v1.1) to track performance changes over the semester.", style_normal))

    # =========================================================================
    # 8. Testing Strategy
    # =========================================================================
    story.append(Paragraph("8. Testing Strategy", style_h1))
    
    # Timeline Chart
    time_img_path = os.path.join(DIAGRAMS_DIR, '06_timeline.png')
    if os.path.exists(time_img_path):
        story.append(Image(time_img_path, width=5*inch, height=3*inch))
        story.append(Paragraph("<i>Figure 6: Expected Model Performance (Simulated)</i>", styles['Normal']))
    
    story.append(Paragraph("Validation ensures F1-score > 0.65 before model deployment.", style_normal))

    story.append(PageBreak())

    # =========================================================================
    # Appendices
    # =========================================================================
    story.append(Paragraph("Appendix A: Feature Dictionary", style_h1))
    # ... (Simplified table for Master doc, full details in separate PDF if needed, but here we include essential list)
    feat_data = [
        ['Feature', 'Description'],
        ['action_cnt', 'Total interactions'],
        ['session_cnt', 'Total study sessions'],
        ['entropy_daily_cnts', 'Regularity of daily login patterns'],
        ['median_session_len', 'Typical study duration']
    ]
    t_feat = Table(feat_data, colWidths=[2.5*inch, 3.5*inch])
    t_feat.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    story.append(t_feat)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Appendix B: Configuration", style_h1))
    story.append(Paragraph("SESSION_THRESHOLD = 1.5 hours", style_code))
    story.append(Paragraph("RF_N_ESTIMATORS = 200", style_code))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Appendix C: Glossary", style_h1))
    glossary_list = ListFlowable([
        ListItem(Paragraph("<b>Sessionization:</b> The process of grouping raw events into meaningful study periods.", style_normal)),
        ListItem(Paragraph("<b>Entropy:</b> A statistical measure of randomness used here to proxy study consistency.", style_normal)),
        ListItem(Paragraph("<b>FERPA:</b> Family Educational Rights and Privacy Act.", style_normal)),
    ], bulletType='bullet')
    story.append(glossary_list)

    # Build PDF
    try:
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        print(f'Successfully created Master SDD: {PDF_PATH}')
        print(f'File size: {os.path.getsize(PDF_PATH)} bytes')
        return True
    except Exception as e:
        print(f'Error creating PDF: {e}')
        return False

if __name__ == '__main__':
    create_master_sdd()
