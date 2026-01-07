#!/usr/bin/env python3
"""
Ch07 SDD Diagrams Generator
Generates all 6 required diagrams for the SDD using Graphviz and Matplotlib.
"""

import os
import graphviz
import matplotlib.pyplot as plt
import numpy as np

# Create diagrams directory
OUTPUT_DIR = 'diagrams'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_context_diagram():
    """1. System Context Diagram"""
    dot = graphviz.Digraph('context', format='png')
    dot.attr(rankdir='LR', dpi='300')
    dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
    
    dot.node('Moodle', 'Moodle LMS\n(External System)', shape='box', fillcolor='lightgrey')
    dot.node('System', 'Learning Analytics\nPrediction System\n(Ch07)', shape='box', fillcolor='lightblue', height='1.5')
    dot.node('Users', 'Instructors /\nAdministrators', shape='ellipse', fillcolor='lightyellow')
    dot.node('Students', 'Students', shape='ellipse', fillcolor='lightyellow')
    
    dot.edge('Moodle', 'System', label='Raw Event Logs\nGradebook Data')
    dot.edge('System', 'Users', label='Prediction Dashboards\nRisk Reports')
    dot.edge('Users', 'Students', label='Interventions\nFeedback')
    
    output_path = os.path.join(OUTPUT_DIR, '01_system_context')
    dot.render(output_path, cleanup=True)
    print(f"Created {output_path}.png")

def create_component_diagram():
    """2. Component Diagram"""
    dot = graphviz.Digraph('component', format='png')
    dot.attr(rankdir='TB', dpi='300')
    dot.attr('node', shape='component', style='filled', fillcolor='white')
    
    with dot.subgraph(name='cluster_pipeline') as c:
        c.attr(label='Prediction Pipeline', style='dashed')
        c.node('Ingest', 'Data Ingestion')
        c.node('Preproc', 'Preprocessing')
        c.node('Session', 'Sessionization')
        c.node('FeatEng', 'Feature\nEngineering')
        c.node('Train', 'Model Training\n(Random Forest)')
        c.node('Predict', 'Prediction &\nEvaluation')
        
        c.edge('Ingest', 'Preproc')
        c.edge('Preproc', 'Session')
        c.edge('Session', 'FeatEng')
        c.edge('FeatEng', 'Train', label='Training Data')
        c.edge('FeatEng', 'Predict', label='Test Data')
        c.edge('Train', 'Predict', label='Trained Model')
        
    output_path = os.path.join(OUTPUT_DIR, '02_component_diagram')
    dot.render(output_path, cleanup=True)
    print(f"Created {output_path}.png")

def create_dfd():
    """3. Data Flow Diagram (Level 1)"""
    dot = graphviz.Digraph('dfd', format='png')
    dot.attr(rankdir='LR', dpi='300')
    
    # Entities
    dot.attr('node', shape='box3d', style='filled', fillcolor='lightgrey')
    dot.node('Moodle', 'Moodle')
    
    # Processes
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightblue')
    dot.node('P1', '1.0\nExtract Data')
    dot.node('P2', '2.0\nSessionize')
    dot.node('P3', '3.0\nCompute Features')
    dot.node('P4', '4.0\nTrain Model')
    dot.node('P5', '5.0\nPredict')
    
    # Data Stores
    dot.attr('node', shape='note', style='filled', fillcolor='white')
    dot.node('DS1', 'Events.xlsx')
    dot.node('DS2', 'Sessions')
    dot.node('DS3', 'Features.pkl')
    dot.node('DS4', 'Predictions.csv')
    
    # Edges
    dot.edge('Moodle', 'P1')
    dot.edge('P1', 'DS1')
    dot.edge('DS1', 'P2')
    dot.edge('P2', 'DS2')
    dot.edge('DS2', 'P3')
    dot.edge('P3', 'DS3')
    dot.edge('DS3', 'P4')
    dot.edge('P4', 'P5', label='Model')
    dot.edge('DS3', 'P5')
    dot.edge('P5', 'DS4')
    
    output_path = os.path.join(OUTPUT_DIR, '03_data_flow')
    dot.render(output_path, cleanup=True)
    print(f"Created {output_path}.png")

def create_erd():
    """4. Entity Relationship Diagram"""
    dot = graphviz.Digraph('erd', format='png')
    dot.attr(rankdir='BT', dpi='300', nodesep='0.5')
    dot.attr('node', shape='record', style='filled', fillcolor='white')
    
    dot.node('Events', '{Events|PK user\nPK ts|+ action\n+ session_id (FK)}')
    dot.node('Sessions', '{Sessions|PK session_id|+ user (FK)\n+ start_time\n+ duration}')
    dot.node('Features', '{Features|PK user\nPK week|+ action_cnt_*\n+ entropy\n+ session_stats}')
    dot.node('Results', '{Results|PK user|+ final_grade\n+ outcome}')
    dot.node('Predictions', '{Predictions|PK user\nPK week|+ pred_outcome\n+ probability\n+ model_ver}')
    
    dot.edge('Events', 'Sessions', label='aggr to', arrowtail='crow', dir='back')
    dot.edge('Events', 'Features', label='computes', arrowtail='crow', dir='back')
    dot.edge('Features', 'Predictions', label='generates', arrowtail='one', dir='back')
    dot.edge('Results', 'Predictions', label='validates', style='dashed')
    dot.edge('Events', 'Results', label='outcome of')
    
    output_path = os.path.join(OUTPUT_DIR, '04_erd')
    dot.render(output_path, cleanup=True)
    print(f"Created {output_path}.png")

def create_pipeline_diagram():
    """5. Feature Engineering Pipeline"""
    dot = graphviz.Digraph('pipeline', format='png')
    dot.attr(rankdir='TD', dpi='300')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow')
    
    dot.node('Raw', 'Raw Event Stream')
    dot.node('Sort', 'Sort by User/Time')
    dot.node('Sess', 'Sessionization\n(Diff > 1.5h)')
    
    # Branches
    dot.node('ActCnt', 'Branch 1\nAction Counts')
    dot.node('Temp', 'Branch 2\nTemporal Stats')
    dot.node('Ent', 'Branch 3\nEntropy')
    
    dot.node('Merge', 'Merge Features')
    dot.node('Norm', 'Standard Scaler')
    dot.node('Final', 'Final Feature Vector')
    
    dot.edge('Raw', 'Sort')
    dot.edge('Sort', 'Sess')
    dot.edge('Sess', 'ActCnt')
    dot.edge('Sess', 'Temp')
    dot.edge('Sess', 'Ent')
    
    dot.edge('ActCnt', 'Merge')
    dot.edge('Temp', 'Merge')
    dot.edge('Ent', 'Merge')
    dot.edge('Merge', 'Norm')
    dot.edge('Norm', 'Final')
    
    output_path = os.path.join(OUTPUT_DIR, '05_feature_pipeline')
    dot.render(output_path, cleanup=True)
    print(f"Created {output_path}.png")

def create_timeline_chart():
    """6. Training & Evaluation Timeline (Matplotlib)"""
    weeks = [1, 2, 3, 4, 5]
    acc = [0.55, 0.62, 0.71, 0.78, 0.82]
    f1 = [0.52, 0.60, 0.70, 0.76, 0.80]
    r2 = [0.10, 0.25, 0.40, 0.55, 0.65]

    plt.figure(figsize=(10, 6))
    plt.plot(weeks, acc, marker='o', label='Accuracy (Class)')
    plt.plot(weeks, f1, marker='s', label='F1-Score (Class)')
    plt.plot(weeks, r2, marker='^', linestyle='--', label='R2 Score (Reg)')
    
    plt.title('Model Performance Evolution by Course Week', fontsize=14)
    plt.xlabel('Course Week', fontsize=12)
    plt.ylabel('Score (0-1)', fontsize=12)
    plt.ylim(0, 1.0)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    
    plt.annotate('F1 Plateaus', xy=(4, 0.76), xytext=(4.2, 0.65),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    output_path = os.path.join(OUTPUT_DIR, '06_timeline.png')
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Created {output_path}")

if __name__ == '__main__':
    create_context_diagram()
    create_component_diagram()
    create_dfd()
    create_erd()
    create_pipeline_diagram()
    create_timeline_chart()
