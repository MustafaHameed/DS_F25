/**
 * Learning Analytics Dashboard - Chart Generation Module
 * Uses Plotly.js for interactive visualizations
 */

/**
 * Create risk distribution timeline chart
 */
function createRiskTimelineChart() {
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'];
    
    const highRiskData = [5, 7, 8, 10, 12, 15, 14, 16];
    const mediumRiskData = [12, 15, 14, 16, 18, 17, 20, 19];
    const lowRiskData = [83, 78, 78, 74, 70, 68, 66, 65];
    
    const trace1 = {
        x: weeks,
        y: highRiskData,
        name: 'High Risk',
        type: 'scatter',
        mode: 'lines+markers',
        stackgroup: 'one',
        fillcolor: 'rgba(231, 76, 60, 0.6)',
        line: {color: '#e74c3c', width: 2},
        marker: {size: 8}
    };
    
    const trace2 = {
        x: weeks,
        y: mediumRiskData,
        name: 'Medium Risk',
        type: 'scatter',
        mode: 'lines+markers',
        stackgroup: 'one',
        fillcolor: 'rgba(243, 156, 18, 0.6)',
        line: {color: '#f39c12', width: 2},
        marker: {size: 8}
    };
    
    const trace3 = {
        x: weeks,
        y: lowRiskData,
        name: 'Low Risk',
        type: 'scatter',
        mode: 'lines+markers',
        stackgroup: 'one',
        fillcolor: 'rgba(39, 174, 96, 0.6)',
        line: {color: '#27ae60', width: 2},
        marker: {size: 8}
    };
    
    const layout = {
        yaxis: {title: 'Number of Students'},
        hovermode: 'x unified',
        showlegend: true,
        legend: {x: 0, y: 1.1, orientation: 'h'},
        margin: {l: 50, r: 30, t: 30, b: 50}
    };
    
    Plotly.newPlot('riskTimeline', [trace3, trace2, trace1], layout, {responsive: true});
}

/**
 * Create activity heatmap
 */
function createActivityHeatmap() {
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const hours = ['12AM', '2AM', '4AM', '6AM', '8AM', '10AM', '12PM', '2PM', '4PM', '6PM', '8PM', '10PM'];
    
    // Generate sample activity data
    const data = [];
    for (let i = 0; i < 7; i++) {
        const row = [];
        for (let j = 0; j < 12; j++) {
            // More activity during daytime hours (8AM-10PM) and weekdays
            let baseActivity = 10;
            if (j >= 4 && j <= 10) baseActivity = 50; // Daytime boost
            if (i < 5) baseActivity *= 1.5; // Weekday boost
            row.push(Math.floor(baseActivity + Math.random() * 20));
        }
        data.push(row);
    }
    
    const trace = {
        z: data,
        x: hours,
        y: days,
        type: 'heatmap',
        colorscale: [
            [0, '#f0f4f8'],
            [0.5, '#3385d6'],
            [1, '#0066cc']
        ],
        hoverongaps: false,
        hovertemplate: '%{y}<br>%{x}<br>Activity: %{z}<extra></extra>'
    };
    
    const layout = {
        xaxis: {title: 'Time of Day'},
        yaxis: {title: 'Day of Week'},
        margin: {l: 80, r: 30, t: 30, b: 50}
    };
    
    Plotly.newPlot('activityHeatmap', [trace], layout, {responsive: true});
}

/**
 * Create model performance chart
 */
function createModelPerformanceChart() {
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'];
    
    const accuracy = [0.82, 0.84, 0.85, 0.86, 0.87, 0.88, 0.87, 0.89];
    const precision = [0.78, 0.80, 0.82, 0.83, 0.84, 0.85, 0.85, 0.86];
    const recall = [0.75, 0.77, 0.79, 0.81, 0.82, 0.83, 0.82, 0.84];
    const f1Score = [0.76, 0.78, 0.80, 0.82, 0.83, 0.84, 0.83, 0.85];
    
    const traces = [
        {x: weeks, y: accuracy, name: 'Accuracy', type: 'scatter', mode: 'lines+markers', line: {width: 2}},
        {x: weeks, y: precision, name: 'Precision', type: 'scatter', mode: 'lines+markers', line: {width: 2}},
        {x: weeks, y: recall, name: 'Recall', type: 'scatter', mode: 'lines+markers', line: {width: 2}},
        {x: weeks, y: f1Score, name: 'F1 Score', type: 'scatter', mode: 'lines+markers', line: {width: 2}}
    ];
    
    const layout = {
        yaxis: {title: 'Score', range: [0.7, 0.95]},
        hovermode: 'x unified',
        showlegend: true,
        legend: {x: 0, y: 1.1, orientation: 'h'},
        margin: {l: 50, r: 30, t: 30, b: 50}
    };
    
    Plotly.newPlot('modelPerformance', traces, layout, {responsive: true});
}

/**
 * Create prediction distribution chart
 */
function createPredictionDistribution() {
    const data = [{
        values: [65, 19, 16],
        labels: ['Low Risk', 'Medium Risk', 'High Risk'],
        type: 'pie',
        marker: {
            colors: ['#27ae60', '#f39c12', '#e74c3c']
        },
        textinfo: 'label+percent',
        hoverinfo: 'label+value+percent'
    }];
    
    const layout = {
        showlegend: true,
        margin: {l: 30, r: 30, t: 30, b: 30}
    };
    
    Plotly.newPlot('predictionDistribution', data, layout, {responsive: true});
}

/**
 * Create confusion matrix
 */
function createConfusionMatrix() {
    const z = [
        [45, 3, 2],  // Actual Low
        [5, 12, 2],  // Actual Medium
        [1, 2, 13]   // Actual High
    ];
    
    const trace = {
        z: z,
        x: ['Predicted Low', 'Predicted Medium', 'Predicted High'],
        y: ['Actual Low', 'Actual Medium', 'Actual High'],
        type: 'heatmap',
        colorscale: 'Blues',
        showscale: true,
        hovertemplate: '%{y}<br>%{x}<br>Count: %{z}<extra></extra>'
    };
    
    const layout = {
        xaxis: {side: 'bottom'},
        yaxis: {autorange: 'reversed'},
        margin: {l: 100, r: 30, t: 30, b: 80}
    };
    
    Plotly.newPlot('confusionMatrix', [trace], layout, {responsive: true});
}

/**
 * Create feature importance chart
 */
function createFeatureImportanceChart() {
    const features = [
        'Total Time Spent',
        'Assignment Completion Rate',
        'Forum Participation',
        'Video Watch Time',
        'Quiz Scores',
        'Login Frequency',
        'Resource Access Count',
        'Peer Interaction',
        'Assignment Submission Timeliness',
        'Discussion Quality Score'
    ];
    
    const importance = [0.185, 0.165, 0.142, 0.128, 0.115, 0.092, 0.078, 0.055, 0.025, 0.015];
    
    const trace = {
        x: importance,
        y: features,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: '#0066cc',
            line: {color: '#004c99', width: 1}
        },
        hovertemplate: '%{y}<br>Importance: %{x:.3f}<extra></extra>'
    };
    
    const layout = {
        xaxis: {title: 'Importance Score'},
        margin: {l: 180, r: 30, t: 30, b: 50},
        yaxis: {autorange: 'reversed'}
    };
    
    Plotly.newPlot('featureImportance', [trace], layout, {responsive: true});
}

/**
 * Create correlation matrix
 */
function createCorrelationMatrix() {
    const features = ['Time', 'Assignments', 'Forum', 'Video', 'Quiz', 'Login'];
    
    const corrMatrix = [
        [1.00, 0.75, 0.62, 0.58, 0.71, 0.65],
        [0.75, 1.00, 0.55, 0.48, 0.82, 0.59],
        [0.62, 0.55, 1.00, 0.43, 0.51, 0.68],
        [0.58, 0.48, 0.43, 1.00, 0.46, 0.52],
        [0.71, 0.82, 0.51, 0.46, 1.00, 0.61],
        [0.65, 0.59, 0.68, 0.52, 0.61, 1.00]
    ];
    
    const trace = {
        z: corrMatrix,
        x: features,
        y: features,
        type: 'heatmap',
        colorscale: [
            [0, '#e74c3c'],
            [0.5, '#f0f4f8'],
            [1, '#0066cc']
        ],
        zmid: 0,
        showscale: true,
        hovertemplate: '%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>'
    };
    
    const layout = {
        xaxis: {side: 'bottom'},
        yaxis: {autorange: 'reversed'},
        margin: {l: 80, r: 30, t: 30, b: 80}
    };
    
    Plotly.newPlot('correlationMatrix', [trace], layout, {responsive: true});
}

/**
 * Create feature distributions chart
 */
function createFeatureDistributions() {
    const trace1 = {
        x: Array.from({length: 50}, () => Math.random() * 100),
        name: 'Total Time Spent (hrs)',
        type: 'histogram',
        opacity: 0.7,
        marker: {color: '#0066cc'}
    };
    
    const trace2 = {
        x: Array.from({length: 50}, () => 40 + Math.random() * 60),
        name: 'Assignment Completion (%)',
        type: 'histogram',
        opacity: 0.7,
        marker: {color: '#27ae60'}
    };
    
    const layout = {
        barmode: 'overlay',
        xaxis: {title: 'Value'},
        yaxis: {title: 'Frequency'},
        showlegend: true,
        legend: {x: 0.6, y: 1},
        margin: {l: 50, r: 30, t: 30, b: 50}
    };
    
    Plotly.newPlot('featureDistributions', [trace1, trace2], layout, {responsive: true});
}
