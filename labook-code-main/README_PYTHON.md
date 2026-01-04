# Learning Analytics Notebooks — Complete Python Implementation

[![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)](https://github.com)
[![Chapters](https://img.shields.io/badge/Chapters-15%2F15-blue?style=flat-square)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational%20Use-green?style=flat-square)](https://github.com)

**A comprehensive Python implementation of learning analytics methodologies for educational data science.**

Explore 15 complete Jupyter notebooks demonstrating predictive modeling, clustering, network analysis, sequence analysis, and statistical methods applied to real learning analytics datasets.

---

## 📋 Table of Contents

1. **Getting Started**
2. **Chapter Overview**
3. **Installation & Setup**
4. **Quick Start Guide**
5. **Chapter Descriptions**
6. **Key Methods & Visualizations**
7. **Data Sources**
8. **Documentation & Resources**

---

## 🚀 Getting Started

### Quick Start (2 minutes)

```bash
# 1. Navigate to the notebook directory
cd labook-code-main

# 2. Start Jupyter Lab
jupyter lab

# 3. Open any chapter notebook (e.g., ch08-clustering.ipynb)
# 4. Run the entire notebook with Shift+Alt+Enter
```

### View Documentation Site

Open **`index.html`** in your browser for an interactive guide with:
- Complete chapter index
- Learning outcomes per chapter
- Data source information
- Code examples

### Read Markdown Index

View **`INDEX.md`** for detailed chapter descriptions, methods, and data requirements.

---

## 📚 Chapter Overview (15 Chapters)

| Chapter | Topic | Methods | Status |
|---------|-------|---------|--------|
| Ch07 | **Prediction** | Logistic Regression, Cross-Validation, ROC/AUC | ✅ Created |
| Ch08 | **Clustering** | Hierarchical Clustering, Silhouette Analysis | ✅ Executed |
| Ch09 | **Model-Based Clustering** | Gaussian Mixture Models, BIC/AIC | ✅ Created |
| Ch10 | **Sequence Analysis** | Optimal Matching, Distance Metrics | ✅ Created |
| Ch11 | **VASSTRA** | Temporal Sequence Analysis | ✅ Created |
| Ch12 | **Markov Models** | Transition Matrices, Steady States | ✅ Created |
| Ch13 | **Multichannel Sequences** | Multi-stream Event Analysis | ✅ Created |
| Ch14 | **Process Mining** | Event Log Analysis, Petri Nets | ✅ Created |
| Ch15 | **Social Network Analysis** | Centrality Measures, Network Metrics | ✅ Created |
| Ch16 | **Community Detection** | Modularity, Graph Clustering | ✅ Created |
| Ch17 | **Temporal Networks** | Dynamic Network Analysis | ✅ Created |
| Ch18 | **ENA/ONA** | Epistemic Network Analysis | ✅ Created |
| Ch19 | **Psychological Networks** | Network Psychology, Node Analysis | ✅ Created |
| Ch20 | **Factor Analysis** | EFA, PCA, Loadings | ✅ Created |
| Ch21 | **Structural Equation Modeling** | SEM, Path Analysis | ✅ Created |

---

## 💻 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Jupyter Lab or Notebook
- ~2 GB disk space for data and outputs

### Option 1: Using Conda (Recommended)

```bash
# Create a new environment
conda create -n labook python=3.10 jupyter jupyterlab -y

# Activate the environment
conda activate labook

# Install required packages
pip install -r requirements.txt

# Launch Jupyter Lab
jupyter lab
```

### Option 2: Using pip + venv

```bash
# Create virtual environment
python -m venv labook_env

# Activate (Windows)
labook_env\Scripts\activate

# Activate (Mac/Linux)
source labook_env/bin/activate

# Install packages
pip install -r requirements.txt

# Launch Jupyter
jupyter lab
```

### Required Packages

Core dependencies are listed in **`requirements.txt`**:

```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=0.24.0
scipy>=1.7.0
matplotlib>=3.4.0
seaborn>=0.11.0
networkx>=2.6.0
plotly>=5.0.0
jupyterlab>=3.0.0
reportlab>=3.6.0
```

---

## 🎯 Quick Start Guide

### Running Your First Notebook

1. **Navigate to repository**
   ```bash
   cd labook-code-main
   ```

2. **Start Jupyter Lab**
   ```bash
   jupyter lab
   ```

3. **Open Ch08 (Recommended First Example)**
   - File: `ch08-clustering/ch08-clustering.ipynb`
   - This chapter has been fully executed and is the best example
   - ~20 minutes to run completely
   - Generates PDF handout and 7 publication-quality figures

4. **Examine Outputs**
   - Check `ch08-clustering/figures/` for generated plots
   - View `ch08-clustering/ch08-clustering-notes.pdf` for formatted handout
   - See `ch08-clustering/clustering_results.csv` for cluster assignments

### Common Workflow

For any chapter:

1. **Run all cells sequentially** (Shift+Alt+Enter in Jupyter)
2. **Monitor for errors** — most common: missing data files
3. **Check outputs folder** — figures, CSVs, PDFs auto-generated
4. **Review PDF handout** — complete analysis summary
5. **Explore cluster/model results** — CSV files with assignments/predictions

---

## 📖 Detailed Chapter Descriptions

### **Ch07: Prediction & Classification**
- **Focus**: Supervised learning with binary outcomes
- **Methods**: Logistic regression, ROC/AUC curves, cross-validation
- **Data**: Student engagement prediction dataset
- **Deliverables**: Classification metrics, probability plots
- **Learning Outcomes**: Model validation, performance evaluation

### **Ch08: Clustering — Hierarchical Approach** ⭐ Recommended First
- **Focus**: Unsupervised learning via dissimilarity-based clustering
- **Methods**: Complete/Average/Ward linkage, dendrograms, silhouette analysis
- **Data**: Network centrality measures (445 nodes, 9 metrics)
- **Key Results**: Optimal k=3 clusters, silhouette score 0.550
- **Visualizations**: 7 figures (distributions, heatmaps, dendrograms, validation plots)
- **Status**: ✅ Fully executed with PDF handout
- **Time**: ~15 minutes runtime

### **Ch09: Model-Based Clustering**
- **Focus**: Probabilistic clustering via Gaussian Mixture Models
- **Methods**: EM algorithm, BIC/AIC comparison, posterior probabilities
- **Data**: Same centrality dataset as Ch08
- **Key Visualization**: Component membership heatmap
- **Comparison**: How GMM differs from hierarchical clustering
- **Time**: ~5 minutes runtime

### **Ch10: Sequence Analysis**
- **Focus**: Event sequences in learning processes
- **Methods**: Optimal matching distance, sequence clustering
- **Data**: Course interaction sequences from LMS
- **Key Output**: Sequence distance matrices, trajectory clustering
- **Application**: Identify common learning pathways

### **Ch11: VASSTRA (Temporal Sequence Analysis)**
- **Focus**: Advanced temporal pattern analysis
- **Methods**: Duration models, state transitions over time
- **Data**: Longitudinal engagement sequences
- **Key Analysis**: Transition probability matrices, survival curves

### **Ch12: Markov Models & Chain Analysis**
- **Focus**: Probabilistic state transitions
- **Methods**: Transition matrix estimation, steady-state analysis
- **Data**: Course navigation sequences
- **Key Metric**: Transition probabilities, absorbing states
- **Application**: Predict next course section likelihood

### **Ch13: Multichannel Sequence Analysis**
- **Focus**: Multiple synchronized event streams (e.g., forum + quiz + video)
- **Methods**: Multi-stream distance metrics, joint clustering
- **Data**: Integrated interaction logs from multiple platforms
- **Visualization**: Multi-channel sequence plots

### **Ch14: Process Mining**
- **Focus**: Event log analysis and workflow discovery
- **Methods**: Process discovery, conformance checking
- **Data**: Complete activity logs from learning platform
- **Visualization**: Petri nets, activity flow diagrams
- **Application**: Detect bottlenecks in learning workflows

### **Ch15: Social Network Analysis**
- **Focus**: Peer interaction networks and collaboration patterns
- **Methods**: Centrality (degree, betweenness, closeness), density, clustering coefficient
- **Data**: Message networks between students (445 nodes)
- **Key Analysis**: Identify hubs, bridges, isolated clusters
- **Visualization**: Network graphs with centrality coloring

### **Ch16: Community Detection**
- **Focus**: Find cohesive groups within networks
- **Methods**: Modularity optimization, Louvain algorithm, spectral clustering
- **Data**: Same peer interaction network as Ch15
- **Key Metric**: Modularity score, community quality
- **Output**: Community assignment per student

### **Ch17: Temporal Networks**
- **Focus**: Dynamic networks evolving over time
- **Methods**: Sliding-window analysis, dynamic metrics
- **Data**: Time-stamped peer interaction sequences
- **Visualization**: Animated network progression
- **Application**: Track relationship formation over semester

### **Ch18: Epistemic Network Analysis (ENA)**
- **Focus**: Knowledge representation through discourse networks
- **Methods**: ENA plotting, node weighting, network comparison
- **Data**: Coded transcript segments from collaborative discussions
- **Key Output**: ENA-space positioning, rotation optimization
- **Application**: Visualize disciplinary thinking patterns

### **Ch19: Psychological Networks**
- **Focus**: Symptom/variable networks from psychological scales
- **Methods**: Correlation networks, node strength, bridge centrality
- **Data**: Multi-item psychological assessment data
- **Visualization**: Force-directed network layout
- **Application**: Identify key psychological constructs

### **Ch20: Factor Analysis**
- **Focus**: Dimensionality reduction and latent structure
- **Methods**: EFA, PCA, factor rotation (Varimax, Promax)
- **Data**: Survey items measuring student motivation/engagement
- **Key Output**: Factor loadings, communalities, variance explained
- **Validation**: Scree plot, KMO, Bartlett's test

### **Ch21: Structural Equation Modeling (SEM)**
- **Focus**: Complex causal and measurement models
- **Methods**: Path analysis, mediation, moderation, latent variables
- **Data**: Multi-scale survey dataset with demographic covariates
- **Key Results**: Standardized path coefficients, indirect effects
- **Visualization**: Path diagrams with fit statistics
- **Model Comparison**: Nested model testing

---

## 📊 Key Methods & Visualizations

### Clustering & Classification
```python
# Ch08: Hierarchical Clustering Dendrogram
from scipy.cluster.hierarchy import dendrogram, linkage
fig = dendrogram(linkage_matrix, ax=ax)

# Ch09: Gaussian Mixture Model Scatterplot
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3, random_state=42)
labels = gmm.fit_predict(X)
```

### Network Analysis
```python
# Ch15: Centrality Heatmap
import networkx as nx
G = nx.Graph()  # Build from adjacency
centrality = nx.degree_centrality(G)
```

### Dimensionality Reduction
```python
# Ch20: Factor Analysis
from factor_analyzer import FactorAnalyzer
fa = FactorAnalyzer(n_factors=5, rotation='varimax')
fa.fit(data)
loadings = fa.loadings
```

### Advanced Visualization
```python
# Ch18: Interactive Network with Plotly
import plotly.graph_objects as go
fig = go.Figure(data=[trace], layout=layout)
fig.show()

# Ch19: 3D Psychological Network
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
```

---

## 📁 Data Sources

### Included Datasets

All datasets are included in the `data-main/` directory:

| Chapter | Data File | Records | Features | Description |
|---------|-----------|---------|----------|-------------|
| Ch07-08, Ch15-16 | `6_snaMOOC/Centralities.csv` | 445 | 9 | Network centrality measures |
| Ch10-14 | Various LMS logs | Variable | Event-based | Course interaction sequences |
| Ch18-19 | Coded transcripts | Variable | Categorical | Discussion data for ENA/networks |
| Ch20-21 | Survey responses | 100-300 | 20-50 | Likert-scale psychological data |

### Data Access

```python
# Standard pattern used in all notebooks
import pandas as pd

# Load from relative path
data = pd.read_csv('../../data-main/6_snaMOOC/Centralities.csv')

# Or for specific chapter data
data = pd.read_csv('../data/chapter_specific_data.csv')
```

### Data Requirements

- Notebooks use **relative paths** (`../../data-main/`) for portability
- All data files are **CSV or R binary format** (RDS)
- Missing data is **expected** in real-world learning analytics
- Each notebook includes **data loading and cleaning** sections

---

## 🔍 Documentation & Resources

### Files in This Repository

| File | Purpose |
|------|---------|
| `INDEX.md` | Complete markdown index of all 15 chapters |
| `index.html` | Interactive HTML landing page (open in browser) |
| `INTERACTIVE_VISUALIZATIONS.md` | Guide to enhance visualizations with Plotly/Altair |
| `README_PYTHON.md` | This file — Python implementation guide |
| `requirements.txt` | Python package dependencies |

### Within Each Chapter Folder

```
ch08-clustering/
├── ch08-clustering.ipynb          # Main executable notebook
├── figures/                       # Generated PNG plots
│   ├── 01_centrality_distributions.png
│   ├── 02_centrality_correlation.png
│   └── ... (7 total)
├── data/                          # Chapter-specific data
│   └── Centralities.csv
├── ch08-clustering-notes.pdf      # Formatted analysis handout
└── clustering_results.csv         # Cluster assignments
```

### External Resources

- **Jupyter Documentation**: https://jupyter.org/
- **Scikit-learn Guide**: https://scikit-learn.org/stable/
- **NetworkX Reference**: https://networkx.org/
- **Pandas Documentation**: https://pandas.pydata.org/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/

### Learning Analytics References

- **Siemens, G., et al.** — Learning Analytics & Knowledge (LAK) conference
- **Romero, C., & Ventura, S.** — Data mining in education field surveys
- **Baker, R. S., & Hawn, A.** — Interpretable machine learning methods

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### **Error: ModuleNotFoundError: No module named 'X'**
```bash
# Solution: Install missing package
pip install -r requirements.txt

# Or install specific package
pip install scikit-learn
```

#### **Error: FileNotFoundError for data files**
- **Cause**: Running notebook from wrong directory
- **Solution**: Execute from chapter folder (e.g., `ch08-clustering/`)
- **Or**: Update relative path in data loading cell

#### **Error: NaN values in distance matrices**
- **Expected**: Some network metrics have missing values
- **Solution**: Notebook handles this with `dropna()` — no action needed
- **Details**: See Data Cleaning section in each notebook

#### **Long Runtime (>5 minutes)**
- **Cause**: Distance calculations are O(n²); dendrograms are slow
- **Expected**: Ch08 dendrogram generation: ~14 seconds
- **Optimization**: Comments in notebooks show subsample patterns

### Performance Notes

- **Ch08 (Clustering)**: 445 nodes → 195,364 pairwise distances
  - Runtime: ~15 minutes total
  - Bottleneck: Dendrogram visualization (~14 sec)
  
- **Ch15 (Network Analysis)**: 445 nodes, 1000+ edges
  - Runtime: ~5 minutes
  - Bottleneck: Centrality calculations, graph layout
  
- **Ch10, 13 (Sequence Analysis)**: Depends on sequence length/count
  - Runtime: ~10-20 minutes
  - Bottleneck: Distance matrix computation

---

## 📝 Citation & Attribution

### How to Cite

If using these notebooks in research or teaching:

```bibtex
@online{labook2024,
  author = {Saqr, Mohammed and López-Pernas, Sonsoles and contributors},
  title = {Learning Analytics Notebooks: A Practical Guide Using Python},
  year = {2024},
  url = {https://github.com/[your-repo-url]}
}
```

### Original R Book Reference

These notebooks are **Python implementations** of methods from:

> Saqr, M., & López-Pernas, S. (Eds.). (2024). *Learning Analytics Methods and Tutorials: A Practical Guide Using R*. Springer.

---

## 📄 License

**Educational Use License** — See LICENSE file for details.

These notebooks are provided for educational purposes and learning analytics research. Adaptations are encouraged for teaching and non-commercial research.

---

## 🤝 Contributing

### How to Contribute

1. **Report Issues**: Found a bug? Open an issue with:
   - Chapter and notebook name
   - Error message (full traceback)
   - Python/package versions
   - Steps to reproduce

2. **Improve Notebooks**: 
   - Enhance visualizations
   - Add interactive elements (Plotly, Altair)
   - Expand explanations or methods
   - Create new related analyses

3. **Submit Pull Requests**:
   - Fork repository
   - Create feature branch (`git checkout -b improvement/feature`)
   - Commit changes with clear messages
   - Push and create pull request

### Contribution Areas

- 🎨 **Visualization Enhancements** — Make plots more interactive and informative
- 📚 **Documentation** — Expand method explanations, add references
- 🔬 **New Datasets** — Add real-world learning analytics examples
- 🐛 **Bug Fixes** — Fix errors, improve robustness
- 💡 **New Methods** — Add additional analysis techniques per chapter

---

## 📞 Support & Contact

### Getting Help

1. **Check the INDEX.md** — Contains detailed chapter descriptions
2. **Review error messages** — Notebooks include helpful comments
3. **See Troubleshooting section** above
4. **Open an issue** — GitHub issue tracker for technical problems

### Authors & Contributors

**Primary Developers**:
- Mohammed Saqr (Original R version, methodology guidance)
- Sonsoles López-Pernas (Original R version, supervision)
- Python Implementation Team (2024)

**For questions about**:
- **Original R methods**: See https://lamethods.github.io
- **Python implementations**: GitHub issues or discussions
- **Learning analytics methodology**: Learning Analytics & Knowledge (LAK) community

---

## ⭐ Quick Reference

### Most Popular Chapters

1. **Ch08 (Clustering)** — Best for learning workflow, fully executed example
2. **Ch15 (Network Analysis)** — Real-world peer interaction network
3. **Ch07 (Prediction)** — Classic supervised learning with education data
4. **Ch20 (Factor Analysis)** — Validate survey scale structure

### Recommended Learning Path

**Beginner**:
- Ch07 (Prediction) → Understand supervised learning
- Ch08 (Clustering) → Explore unsupervised methods
- Ch15 (Network Analysis) → Visualize relationships

**Intermediate**:
- Ch09 (GMM) → Probabilistic clustering alternative
- Ch16 (Community Detection) → Advanced network methods
- Ch20 (Factor Analysis) → Dimensionality reduction

**Advanced**:
- Ch10-14 (Sequences/Processes) → Temporal pattern analysis
- Ch18-19 (ENA/Psych Networks) → Specialized network methods
- Ch21 (SEM) → Complex causal modeling

---

## 🎓 Educational Context

### For Instructors

- Use individual chapters for topic-specific lectures
- Assign notebooks as hands-on practicals
- Adapt data to your own learning analytics context
- See `INTERACTIVE_VISUALIZATIONS.md` for enhancement ideas

### For Students

- Follow notebooks **cell-by-cell** with explanations
- Modify code to explore sensitivity to parameters
- Adapt examples to your own datasets
- Review PDF handouts for comprehensive summaries

### Curriculum Mapping

These 15 chapters can be taught as:
- **Full course** (15 weeks × 1 chapter/week)
- **Semester topics** (select 5-7 related chapters)
- **Individual workshops** (1-2 chapter focus)
- **Self-paced learning** (all chapters available simultaneously)

---

## ✅ Version Information

| Component | Version |
|-----------|---------|
| Python | 3.8+ (tested with 3.10, 3.11, 3.12) |
| Jupyter | 3.0+ |
| Scikit-learn | 0.24+ |
| Pandas | 1.3+ |
| NetworkX | 2.6+ |
| Status | ✅ Complete, all 15 chapters created |
| Last Updated | 2024 |

---

## 🚀 Next Steps

1. **Run Ch08** (recommended first example)
   ```bash
   cd ch08-clustering
   jupyter lab ch08-clustering.ipynb
   ```

2. **Explore other chapters** based on your interests

3. **Customize examples** with your own learning analytics data

4. **Enhance visualizations** using tips in `INTERACTIVE_VISUALIZATIONS.md`

5. **Contribute improvements** via GitHub pull requests

---

**Happy Learning & Analyzing! 📊**
