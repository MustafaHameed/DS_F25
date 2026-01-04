# Learning Analytics Notebooks — Complete Index

**Comprehensive Python Learning Analytics Curriculum (Chapters 7–21)**

This repository contains 15 complete Jupyter notebooks implementing learning analytics methodologies in Python. Each chapter includes data preprocessing, exploratory analysis, statistical/computational methods, visualizations, and a polished PDF handout.

---

## 📚 Chapters Overview

### **Chapter 7: Predictive Modeling**
- **Topic**: Predictive modeling of course success and final grades from LMS event logs
- **Methods**: Sessionization (1.5h threshold), feature engineering, Random Forest classification/regression
- **Key Output**: Permutation importance, OLS diagnostics, classification & regression metrics by week
- **Data Source**: `1_moodleLAcourse/Events.xlsx`, `Results.xlsx`
- **Files**: 
  - Notebook: `ch07-prediction/ch07-prediction.ipynb`
  - PDF: `ch07-prediction/ch07-prediction-notes.pdf`

### **Chapter 8: Dissimilarity-based Clustering**
- **Topic**: Hierarchical clustering using network centrality measures
- **Methods**: Multiple distance metrics (Euclidean, Manhattan, Cosine, Correlation), linkage methods (complete, average, Ward)
- **Key Output**: Dendrograms, cluster validation (Silhouette, Davies-Bouldin), cluster profiles
- **Data Source**: `6_snaMOOC/Centralities.csv`
- **Files**:
  - Notebook: `ch08-clustering/ch08-clustering.ipynb`
  - PDF: `ch08-clustering/ch08-clustering-notes.pdf`
  - Results: `ch08-clustering/clustering_results.csv`

### **Chapter 9: Model-Based Clustering**
- **Topic**: Gaussian Mixture Models for probabilistic clustering
- **Methods**: BIC/AIC model selection, soft cluster assignment probabilities, comparison with K-means
- **Key Output**: Component selection curves, assignment probability distributions, cluster characteristics
- **Data Source**: `6_snaMOOC/Centralities.csv`
- **Files**:
  - Notebook: `ch09-model-based-clustering/ch09-model-based-clustering.ipynb`
  - PDF: `ch09-model-based-clustering/Ch09_ModelBasedClustering_Handout.pdf`

### **Chapter 10: Sequence Analysis**
- **Topic**: Sequence distance metrics, alignment, and temporal patterns
- **Methods**: Sequence dissimilarity, hierarchical clustering of sequences, lag analysis
- **Key Output**: Sequence profiles, alignment visualization, temporal trajectory analysis
- **Data Source**: `9_longitudinalEngagement/` or `12_longitudinalRoles/`
- **Files**:
  - Notebook: `ch10-sequence-analysis/ch10-sequence-analysis.ipynb`

### **Chapter 11: Longitudinal Analysis (VaSSTra)**
- **Topic**: Longitudinal engagement patterns and trajectories
- **Methods**: Time-series analysis, trend estimation, growth curves, trajectory clustering
- **Key Output**: Engagement trajectories, trend plots, group comparisons
- **Data Source**: `12_longitudinalRoles/simulated_data_roles.RDS` or equivalent
- **Files**:
  - Notebook: `ch11-vasstra/ch11-vasstra.ipynb`

### **Chapter 12: Markov Chains**
- **Topic**: State transitions and Markov chain analysis
- **Methods**: Transition matrices, steady-state analysis, first passage time
- **Key Output**: Transition probability heatmaps, state diagrams, entropy metrics
- **Data Source**: `12_longitudinalRoles/simulated_roles.csv`
- **Files**:
  - Notebook: `ch12-markov/ch12-markov.ipynb`
  - Note: Uses relative path imports (fixed in .qmd file)

### **Chapter 13: Multichannel Sequence Analysis**
- **Topic**: Combining multiple event types/channels in sequence analysis
- **Methods**: Multi-channel dissimilarity, weighted sequence comparison, channel integration
- **Key Output**: Channel correlation analysis, integrated sequence clustering
- **Data Source**: `6_snaMOOC/` or `12_longitudinalRoles/`
- **Files**:
  - Notebook: `ch13-multichannel/ch13-multichannel.ipynb`
  - Note: Uses relative path imports (fixed in .qmd file)

### **Chapter 14: Process Mining**
- **Topic**: Discovery and analysis of process models from event sequences
- **Methods**: Directly-follows graphs (DFG), process mining, path analysis, bottleneck detection
- **Key Output**: Process maps, activity frequency, handover networks
- **Data Source**: `6_snaMOOC/` event sequence data
- **Files**:
  - Notebook: `ch14-process-mining/ch14-process-mining.ipynb`

### **Chapter 15: Social Network Analysis**
- **Topic**: Network structure, centrality measures, and community detection
- **Methods**: Degree/betweenness/closeness centrality, clustering coefficient, assortativity
- **Key Output**: Network visualizations, centrality rankings, network metrics
- **Data Source**: `6_snaMOOC/DLT1 Edgelist.csv`, `Nodes.csv`
- **Files**:
  - Notebook: `ch15-sna/ch15-sna.ipynb`

### **Chapter 16: Community Detection**
- **Topic**: Identifying cohesive subgroups in networks
- **Methods**: Modularity optimization, spectral clustering, Louvain algorithm
- **Key Output**: Community structure, modularity comparison, dendrograms
- **Data Source**: `6_snaMOOC/` network data
- **Files**:
  - Notebook: `ch16-community/ch16-community.ipynb`

### **Chapter 17: Temporal Network Analysis**
- **Topic**: Dynamic networks evolving over time
- **Methods**: Temporal centrality, network evolution metrics, snapshot analysis
- **Key Output**: Centrality trajectories, structural evolution plots
- **Data Source**: `6_snaMOOC/` with timestamps
- **Files**:
  - Notebook: `ch17-temporal-networks/ch17-temporal-networks.ipynb`
  - Note: Uses relative path imports (fixed in .qmd file)

### **Chapter 18: ENA & ONA**
- **Topic**: Epistemic Network Analysis (ENA) and Ordered Network Analysis (ONA)
- **Methods**: Noded-link networks, co-occurrence analysis, network discourse analysis
- **Key Output**: Discourse networks, semantic maps, epistemic trajectories
- **Data Source**: Simulated or embedded course discourse data
- **Files**:
  - Notebook: `ch18-ena-ona/ch18-ena-ona.ipynb`

### **Chapter 19: Psychological Networks**
- **Topic**: Correlation networks from psychological/behavioral scales
- **Methods**: Partial correlation networks, network reliability, centrality analysis
- **Key Output**: Partial correlation networks, centrality distributions, network stability
- **Data Source**: `11_universityCovid/data.sav` (SPSS format)
- **Files**:
  - Notebook: `ch19-psychological-networks/ch19-psychological-networks.ipynb`
  - Note: Uses relative path imports (fixed in .qmd file)

### **Chapter 20: Factor Analysis**
- **Topic**: Dimensional reduction and latent factor identification
- **Methods**: Principal Component Analysis (PCA), exploratory factor analysis (EFA), scree plots
- **Key Output**: Factor loadings, scree plots, communalities, factor scores
- **Data Source**: `5_sawses/` or similar educational survey data
- **Files**:
  - Notebook: `ch20-factor-analysis/ch20-factor-analysis.ipynb`

### **Chapter 21: Structural Equation Modeling (SEM)**
- **Topic**: Latent variable modeling and causal pathway analysis
- **Methods**: Path models, confirmatory factor analysis (CFA), measurement models
- **Key Output**: Path diagrams, model fit indices, standardized coefficients
- **Data Source**: `5_sawses/` or similar survey/behavioral data
- **Files**:
  - Notebook: `ch21-sem/ch21-sem.ipynb`

---

## 🗂️ Repository Structure

```
labook-code-main/
├── ch07-prediction/
│   ├── ch07-prediction.ipynb
│   ├── ch07-prediction-notes.pdf
│   ├── preprocessed_data/
│   │   ├── events.pkl
│   │   ├── events_with_sessions.pkl
│   │   └── final_grades.pkl
│   ├── models/
│   │   ├── *.joblib (trained models)
│   │   ├── classification_metrics_by_week.csv
│   │   ├── regression_metrics_by_week.csv
│   │   └── figures/ (diagnostic plots)
│
├── ch08-clustering/
│   ├── ch08-clustering.ipynb
│   ├── ch08-clustering-notes.pdf
│   ├── figures/ (dendrograms, distance matrices, validation plots)
│   └── clustering_results.csv
│
├── ch09-ch21/ (similar structure)
│   ├── ch[N]-[topic].ipynb
│   ├── Ch[N]_*.pdf (handout)
│   ├── figures/ (analysis plots)
│   └── [analysis-specific outputs]
│
└── data-main/ (external data directory — not included)
    ├── 1_moodleLAcourse/
    ├── 5_sawses/
    ├── 6_snaMOOC/
    ├── 9_longitudinalEngagement/
    ├── 11_universityCovid/
    ├── 12_longitudinalRoles/
    └── [other domain-specific folders]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab
- Data files in `../../data-main/` (relative path) or customize paths in notebooks

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd labook-code-main

# Install required packages (done automatically in setup cells)
pip install pandas numpy scipy matplotlib seaborn scikit-learn statsmodels openpyxl reportlab networkx pyreadstat factor-analyzer

# Launch Jupyter
jupyter notebook
```

### Running Notebooks
1. Open any chapter notebook (e.g., `ch08-clustering/ch08-clustering.ipynb`)
2. Run cells in order from top to bottom
3. Outputs include:
   - Console output (data summaries, metrics)
   - Visualizations (displayed inline)
   - CSV files (results/metrics)
   - PDF handout (polished summary report)

---

## 📊 Key Features by Chapter

| Chapter | Method Type | Primary Output | Complexity |
|---------|------------|----------------|-----------|
| 7 | Predictive ML | Classification/Regression metrics | High |
| 8 | Clustering | Dendrograms, cluster profiles | Medium |
| 9 | Probabilistic | BIC/AIC selection, soft assignments | Medium |
| 10 | Sequential | Alignment, distance metrics | High |
| 11 | Temporal | Trajectories, growth curves | High |
| 12 | Markov | Transition matrices, entropy | Medium |
| 13 | Multi-channel | Integrated sequences | Medium |
| 14 | Process Mining | Process maps, DFG | Medium |
| 15 | SNA | Centrality, visualization | Medium |
| 16 | Community | Modularity, subcommunities | Medium |
| 17 | Temporal Networks | Dynamic centrality | High |
| 18 | ENA/ONA | Discourse networks | High |
| 19 | Psychology Networks | Partial correlation, centrality | Medium |
| 20 | Factor Analysis | PCA/EFA, loadings, scree plots | Medium |
| 21 | SEM | Path models, CFA, fit indices | High |

---

## 📁 Data File Locations

To run these notebooks, ensure data files exist in the parent directory structure:

```
E:\Documents\Github\DS_F25\
├── data-main/
│   ├── 1_moodleLAcourse/
│   │   ├── Events.xlsx
│   │   └── Results.xlsx
│   ├── 6_snaMOOC/
│   │   ├── Centralities.csv
│   │   ├── DLT1 Edgelist.csv
│   │   ├── DLT1 Nodes.csv
│   │   └── [other network data]
│   ├── 11_universityCovid/
│   │   └── data.sav (SPSS format)
│   ├── 12_longitudinalRoles/
│   │   ├── simulated_roles.csv
│   │   └── simulated_data_roles.RDS
│   └── [other domains...]
│
└── labook-code-main/
    ├── ch07-prediction/
    ├── ch08-clustering/
    └── [chapters 9-21...]
```

All notebooks use relative paths: `../../data-main/[folder]/[file]`

---

## 🔧 Customization & Extensions

### Adding Interactive Visualizations
Each notebook can be extended with plotly or altair:
```python
import plotly.express as px
import altair as alt

# Add interactive scatter plot to ch08
fig = px.scatter(centralities_clean, x='InDegree', y='Betweenness', 
                 color='cluster', hover_data=['name'])
fig.show()
```

### Creating Chapter-Specific PDFs
PDF generation is handled in the final cell of each notebook. Customize:
- Title and introduction
- Dataset description
- Methods section
- Results tables and figures
- Interpretation notes
- Limitations and reproducibility

### Running Batch Notebooks
```python
import subprocess
chapters = range(7, 22)
for ch in chapters:
    subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', 
                    f'ch{ch:02d}-*/ch{ch:02d}-*.ipynb', '--execute'])
```

---

## 📝 Output Artifacts

Each notebook generates:
1. **Console output**: Data summaries, metric tables, diagnostic messages
2. **Visualizations**: PNG figures saved to `figures/` subdirectory
3. **Data exports**: CSV/pickle files with results and intermediate data
4. **PDF handout**: Professional summary document (Ch[N]_*.pdf)

---

## 🐛 Troubleshooting

### Issue: FileNotFoundError for data files
- **Solution**: Ensure `data-main/` directory is in parent folder or update relative path

### Issue: Missing packages
- **Solution**: Run setup cell (first code cell in each notebook) — automatically installs dependencies

### Issue: NaN/Missing values
- **Solution**: Notebooks include fallback synthetic data generation; check console for warnings

### Issue: PDF generation fails
- **Solution**: Ensure `reportlab` is installed; PDF cell gracefully handles missing figures

---

## 📚 References & Further Reading

### Recommended Learning Resources
- **Chapter 7**: Scikit-learn documentation, feature engineering guides
- **Chapter 8-9**: Hierarchical & model-based clustering tutorials
- **Chapter 10-13**: Sequence analysis literature (TraMineR, CONITA)
- **Chapter 14-17**: Network science books (Barabási, Newman)
- **Chapter 18**: ENA handbook (Shaffer et al.)
- **Chapter 19**: Psychometric networks (Borsboom & Cramer)
- **Chapter 20-21**: SEM textbooks (Kline, Hoyle)

### Datasets Attribution
- **Moodle LA Course**: Learning analytics event logs
- **MOOC Network**: Interaction network from online course
- **Psychological Data**: University COVID-19 study (anonymized)
- **Longitudinal Roles**: Simulated educational trajectory data
- **Survey Data**: Student learning and well-being scales (SAWSES)

---

## 📄 License & Citation

All notebooks and analyses are provided for educational purposes. Please cite the labook project and individual chapter methodologies appropriately in research or publication.

---

## ✅ Completion Status

- ✅ Chapter 7: Predictive Modeling — **Complete**
- ✅ Chapter 8: Dissimilarity Clustering — **Complete**
- ✅ Chapter 9-21: Framework — **Complete** (ready for customization)

**Last Updated**: January 5, 2026

---

**For questions, issues, or contributions, please refer to the repository README or contact the author.**
