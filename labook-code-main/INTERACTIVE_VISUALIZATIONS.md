# Interactive Visualization Enhancement Guide

This guide demonstrates how to enhance the labook notebooks with interactive Plotly and Altair visualizations.

## Overview

The base notebooks include static matplotlib/seaborn visualizations. This guide shows how to add interactive versions using:
- **Plotly**: Interactive 3D plots, hover tooltips, zoom/pan
- **Altair**: Declarative grammar of graphics, linked views
- **Bokeh**: Server-based interactive dashboards

## Installation

```bash
pip install plotly altair bokeh
```

## Chapter 8: Enhanced Clustering Visualization

### Before (Static Dendrogram)
```python
from scipy.cluster.hierarchy import dendrogram
dendrogram(Z_ward, ax=ax)
plt.show()
```

### After (Interactive Dendrogram with Plotly)

Add this cell to `ch08-clustering/ch08-clustering.ipynb` after the dendrogram section:

```python
## Interactive Dendrogram with Plotly

import plotly.figure_factory as ff
import plotly.graph_objects as go

# Create interactive dendrogram
fig = ff.create_dendrogram(
    data_scaled,
    linkagefun=lambda x: linkage(x, method='ward'),
    labels=[f'Node_{i}' for i in range(len(data_scaled))],
    orientation='left',
    color_threshold=50
)

fig.update_layout(
    title='Interactive Hierarchical Clustering Dendrogram (Ward)',
    xaxis_title='Ward Distance',
    yaxis_title='Student/Node',
    hovermode='closest',
    width=1000,
    height=1200,
    font=dict(size=10)
)

fig.write_html('figures/08_interactive_dendrogram.html')
fig.show()

print('Saved interactive dendrogram to figures/08_interactive_dendrogram.html')
```

### Interactive Cluster Scatter Plot

```python
## Interactive Cluster Visualization with Plotly

import plotly.express as px

# Prepare data for plotting (use first two principal components)
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca_coords = pca.fit_transform(data_scaled)

cluster_df = pd.DataFrame({
    'PC1': pca_coords[:, 0],
    'PC2': pca_coords[:, 1],
    'Cluster': cluster_labels,
    'NodeID': [f'Student_{i}' for i in range(len(cluster_labels))],
    'InDegree': centralities_clean['InDegree'].values,
    'Betweenness': centralities_clean['Betweenness'].values
})

# Create interactive scatter plot
fig = px.scatter(
    cluster_df,
    x='PC1',
    y='PC2',
    color='Cluster',
    hover_data=['NodeID', 'InDegree', 'Betweenness'],
    title='Interactive Cluster Visualization (PCA)',
    labels={'PC1': f'PC1 ({pca.explained_variance_ratio_[0]:.1%})',
            'PC2': f'PC2 ({pca.explained_variance_ratio_[1]:.1%})'},
    width=900,
    height=700
)

fig.update_traces(marker=dict(size=8, opacity=0.7))
fig.write_html('figures/08_interactive_clusters.html')
fig.show()

print('Saved interactive cluster plot to figures/08_interactive_clusters.html')
```

### Interactive 3D Scatter Plot

```python
## 3D Interactive Visualization

# Use three key centrality measures
fig = px.scatter_3d(
    centralities_clean,
    x='InDegree',
    y='Betweenness',
    z='Eigen',
    color='cluster',
    hover_data=['name'],
    title='3D Cluster Visualization: Network Centrality Measures',
    labels={'InDegree': 'In-Degree Centrality',
            'Betweenness': 'Betweenness Centrality',
            'Eigen': 'Eigenvector Centrality'},
    width=900,
    height=700
)

fig.write_html('figures/08_interactive_3d_clusters.html')
fig.show()
```

## Chapter 9: Enhanced GMM Visualization

### Interactive BIC/AIC Comparison

```python
## Interactive Model Selection Plot

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(n_components_range),
    y=bic_scores,
    mode='lines+markers',
    name='BIC',
    line=dict(color='#667eea', width=3),
    marker=dict(size=10)
))

fig.add_trace(go.Scatter(
    x=list(n_components_range),
    y=aic_scores,
    mode='lines+markers',
    name='AIC',
    line=dict(color='#f39c12', width=3),
    marker=dict(size=10)
))

fig.add_vline(
    x=optimal_n_bic,
    line_dash='dash',
    line_color='red',
    annotation_text=f'Optimal (k={optimal_n_bic})',
    annotation_position='top right'
)

fig.update_layout(
    title='Interactive BIC/AIC Model Selection',
    xaxis_title='Number of Components',
    yaxis_title='Information Criterion',
    hovermode='x unified',
    width=900,
    height=600,
    template='plotly_white'
)

fig.write_html('figures/09_interactive_bic_aic.html')
fig.show()
```

## Chapter 15: Interactive Network Visualization

### Network Graph with Plotly

```python
## Interactive Network Visualization

# Assuming you have edge list and node data
import networkx as nx
import plotly.graph_objects as go

# Create network graph
G = nx.from_pandas_edgelist(edges_df, 'source', 'target')

# Compute layout
pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

# Extract node positions
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]

# Extract edges
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

# Create figure
fig = go.Figure()

# Add edges
fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode='lines',
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    showlegend=False
))

# Add nodes
fig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    marker=dict(
        size=10,
        color=[centralities_clean.loc[node, 'InDegree'] for node in G.nodes()],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='In-Degree')
    ),
    text=[f'Node: {node}' for node in G.nodes()],
    hovertemplate='%{text}<br>In-Degree: %{marker.color}',
    showlegend=False
))

fig.update_layout(
    title='Interactive Network Visualization',
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    width=1000,
    height=800
)

fig.write_html('figures/15_interactive_network.html')
fig.show()
```

## Chapter 20: Interactive Factor Analysis

### Scree Plot with Interaction

```python
## Interactive Scree Plot with Variance Explained

import plotly.graph_objects as go

cumsum_var = np.cumsum(explained_variance_ratio)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=list(range(1, len(explained_variance_ratio) + 1)),
    y=explained_variance_ratio,
    name='Individual Variance',
    marker_color='#667eea'
))

fig.add_trace(go.Scatter(
    x=list(range(1, len(explained_variance_ratio) + 1)),
    y=cumsum_var,
    name='Cumulative Variance',
    mode='lines+markers',
    line=dict(color='#f39c12', width=3),
    marker=dict(size=8),
    yaxis='y2'
))

fig.update_layout(
    title='Interactive Scree Plot: Variance Explained by Factors',
    xaxis_title='Principal Component',
    yaxis_title='Variance Explained (Individual)',
    yaxis2=dict(title='Cumulative Variance Explained', overlaying='y', side='right'),
    hovermode='x unified',
    width=1000,
    height=600,
    template='plotly_white'
)

fig.write_html('figures/20_interactive_scree.html')
fig.show()
```

## Altair: Linked Visualizations

### Example: Linked Scatter and Histogram

```python
## Linked Visualization with Altair

import altair as alt

# Base selection
brush = alt.selection_interval(encodings=['x', 'y'])

# Scatter plot with selection
scatter = alt.Chart(cluster_df).mark_circle(size=100).encode(
    x='PC1:Q',
    y='PC2:Q',
    color=alt.condition(brush, 'Cluster:N', alt.value('lightgray')),
    tooltip=['NodeID:N', 'InDegree:Q', 'Cluster:N']
).add_selection(
    brush
).properties(
    width=400,
    height=400
)

# Histogram
hist = alt.Chart(cluster_df).mark_bar().encode(
    x=alt.X('InDegree:Q', bin=alt.Bin(maxbins=20)),
    y='count():Q',
    color='Cluster:N'
).transform_filter(
    brush
).properties(
    width=400,
    height=200
)

# Combine
chart = (scatter | hist).properties(title='Interactive Cluster Explorer')
chart.save('figures/08_altair_linked_viz.html')
chart.show()
```

## Best Practices

1. **Save to HTML files**: Use `.write_html()` to create standalone interactive files
2. **Hover information**: Include key metrics in `hoverdata` or `hovertemplate`
3. **Color coding**: Use consistent color schemes across chapters
4. **Performance**: For large datasets (>1000 points), consider sampling or aggregation
5. **Accessibility**: Add titles, axis labels, legends for clarity

## Integration with Notebooks

Add to the setup cell:
```python
# Interactive visualization libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    import altair as alt
    print('Interactive visualization libraries loaded')
except ImportError:
    print('Optional: install plotly and altair for interactive visualizations')
    print('  pip install plotly altair')
```

## Example: Complete Enhanced Notebook Cell

```python
## 8.5 - Interactive Visualizations (Optional)

# Skip this cell if plotly/altair not installed
try:
    import plotly.figure_factory as ff
    import plotly.express as px
    
    # Interactive dendrogram
    fig = ff.create_dendrogram(data_scaled, 
                              linkagefun=lambda x: linkage(x, 'ward'),
                              orientation='left')
    fig.update_layout(title='Interactive Dendrogram', width=1000, height=1200)
    fig.write_html('figures/dendrogram_interactive.html')
    print('✓ Saved interactive dendrogram')
    
    # Interactive scatter plot
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(data_scaled)
    
    df_pca = pd.DataFrame({
        'PC1': pca_data[:, 0],
        'PC2': pca_data[:, 1],
        'Cluster': cluster_labels
    })
    
    fig = px.scatter(df_pca, x='PC1', y='PC2', color='Cluster',
                    title='Interactive Cluster View')
    fig.write_html('figures/clusters_interactive.html')
    print('✓ Saved interactive cluster plot')
    
except ImportError:
    print('⚠ Plotly not installed; skipping interactive visualizations')
    print('  Install with: pip install plotly')
```

## Viewing Interactive Outputs

After running notebook cells with `.write_html()`:

1. **In Jupyter**: Use `IFrame` to embed HTML
```python
from IPython.display import IFrame
IFrame('figures/dendrogram_interactive.html', width=1000, height=600)
```

2. **Standalone**: Open HTML file in web browser directly

3. **Repository**: Add links to HTML files in documentation:
```markdown
- [Interactive Dendrogram](ch08-clustering/figures/dendrogram_interactive.html)
- [3D Cluster Visualization](ch08-clustering/figures/clusters_3d.html)
```

## Summary

These enhancements provide:
- ✅ Hover tooltips with detailed information
- ✅ Zoom, pan, and selection tools
- ✅ 3D visualizations for multi-dimensional data
- ✅ Linked views for exploratory analysis
- ✅ Publication-ready interactive figures
- ✅ Standalone HTML outputs for sharing

Each chapter can be extended similarly based on the specific analysis and visualization needs.
