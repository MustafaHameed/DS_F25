const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleStudents = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});

async function initializeDashboard() {
    setStatus("Loading backend output from outputs/backend/dashboard.json...");

    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });

        if (!response.ok) {
            throw new Error(`Backend output not available. HTTP ${response.status}`);
        }

        dashboardData = await response.json();
        visibleStudents = dashboardData.students || [];

        renderMeta();
        renderOverview();
        renderCharts();
        buildManualInputForm();
        renderStudentsTable(visibleStudents);
        bindFilters();
        runManualPrediction();
        setStatus("Dashboard loaded from generated backend artifacts.");
    } catch (error) {
        console.error(error);
        setStatus("Backend output is missing. Run ./run/run_backend.ps1 and refresh this page.");
    }
}

function renderMeta() {
    const generatedAt = document.getElementById("generatedAt");
    generatedAt.textContent = `Generated: ${dashboardData.project.generated_at}`;
}

function renderOverview() {
    const overview = dashboardData.overview;
    document.getElementById("totalStudents").textContent = overview.total_students;
    document.getElementById("highRisk").textContent = overview.high_risk;
    document.getElementById("bestClassWeek").textContent = `Week ${overview.best_classification_week}`;
    document.getElementById("bestRegWeek").textContent = `Week ${overview.best_regression_week}`;
}

function renderCharts() {
    renderRiskChart();
    renderClassificationChart();
    renderRegressionChart();
    renderFeatureChart();
}

function renderRiskChart() {
    const riskCounts = dashboardData.risk_counts || [];

    Plotly.newPlot("riskChart", [
        {
            type: "bar",
            x: riskCounts.map((item) => titleCase(item.risk_level)),
            y: riskCounts.map((item) => item.count),
            marker: {
                color: ["#c24f2a", "#d3a223", "#0d7a5f"]
            },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Students", gridcolor: "#e8e0d2" },
        xaxis: { title: "Risk Level" }
    }, { responsive: true, displayModeBar: false });
}

function renderClassificationChart() {
    const metrics = dashboardData.classification_metrics || [];

    Plotly.newPlot("classificationChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            name: "Accuracy",
            x: metrics.map((item) => item.week),
            y: metrics.map((item) => item.Accuracy),
            line: { color: "#0d7a5f", width: 3 }
        },
        {
            type: "scatter",
            mode: "lines+markers",
            name: "F1",
            x: metrics.map((item) => item.week),
            y: metrics.map((item) => item.F1),
            line: { color: "#c24f2a", width: 3 }
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Week" },
        yaxis: { title: "Score", gridcolor: "#e8e0d2", range: [0, 1] }
    }, { responsive: true, displayModeBar: false });
}

function renderRegressionChart() {
    const metrics = dashboardData.regression_metrics || [];

    Plotly.newPlot("regressionChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            name: "R2",
            x: metrics.map((item) => item.week),
            y: metrics.map((item) => item.R2),
            line: { color: "#0d7a5f", width: 3 }
        },
        {
            type: "scatter",
            mode: "lines+markers",
            name: "RMSE",
            x: metrics.map((item) => item.week),
            y: metrics.map((item) => item.RMSE),
            yaxis: "y2",
            line: { color: "#64513c", width: 3, dash: "dot" }
        }
    ], {
        margin: { t: 20, r: 50, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Week" },
        yaxis: { title: "R2", gridcolor: "#e8e0d2" },
        yaxis2: {
            title: "RMSE",
            overlaying: "y",
            side: "right"
        },
        legend: { orientation: "h" }
    }, { responsive: true, displayModeBar: false });
}

function renderFeatureChart() {
    const features = dashboardData.top_features?.classification || [];
    const ordered = [...features].reverse();

    Plotly.newPlot("featureChart", [
        {
            type: "bar",
            orientation: "h",
            x: ordered.map((item) => item.importance),
            y: ordered.map((item) => item.feature),
            marker: {
                color: ordered.map((_, index) => index),
                colorscale: [
                    [0, "#d8efe7"],
                    [1, "#0d7a5f"]
                ]
            },
            hovertemplate: "%{y}: %{x}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 150 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Importance", gridcolor: "#e8e0d2" }
    }, { responsive: true, displayModeBar: false });
}

function buildManualInputForm() {
    const manualDemo = dashboardData.manual_demo;
    const form = document.getElementById("manualInputForm");
    form.innerHTML = "";

    if (!manualDemo?.field_schema?.length) {
        form.innerHTML = "<p>Manual forecast inputs are not available in the current backend output.</p>";
        return;
    }

    for (const field of manualDemo.field_schema) {
        const wrapper = document.createElement("div");
        wrapper.className = "input-field";
        wrapper.innerHTML = `
            <label for="field-${field.name}">${field.label}</label>
            <input id="field-${field.name}" name="${field.name}" type="number" step="${field.step}" min="${field.min}" max="${field.max}" value="${field.default}">
            <small>${field.description}</small>
        `;
        form.appendChild(wrapper);
    }

    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Estimate Student Risk";
    form.appendChild(submitButton);

    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.className = "secondary";
    resetButton.textContent = "Reset Defaults";
    resetButton.addEventListener("click", () => {
        for (const field of manualDemo.field_schema) {
            document.getElementById(`field-${field.name}`).value = field.default;
        }
        runManualPrediction();
    });
    form.appendChild(resetButton);

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        runManualPrediction();
    });
}

function runManualPrediction() {
    const manualDemo = dashboardData.manual_demo;
    if (!manualDemo?.feature_order?.length) {
        return;
    }

    const rawInput = manualDemo.feature_order.map((featureName) => Number(document.getElementById(`field-${featureName}`).value));

    const classificationModel = manualDemo.classification_model;
    const regressionModel = manualDemo.regression_model;

    const riskProbability = logisticScore(rawInput, classificationModel);
    const predictedGrade = linearScore(rawInput, regressionModel);
    const thresholds = manualDemo.cohort;

    let riskLevel = "low";
    if (riskProbability >= thresholds.high_risk_threshold) {
        riskLevel = "high";
    } else if (riskProbability >= thresholds.medium_risk_threshold) {
        riskLevel = "medium";
    }

    const outcomeLabel = riskProbability >= 0.5 ? "Low" : "High";
    const gradeDelta = predictedGrade - thresholds.average_grade;
    const deltaLabel = `${gradeDelta >= 0 ? "+" : ""}${gradeDelta.toFixed(2)} vs cohort average`;

    document.getElementById("manualSummary").innerHTML = `
        <strong>${titleCase(riskLevel)} risk forecast</strong>
        Risk probability: ${formatPercent(riskProbability)}<br>
        Predicted outcome: ${outcomeLabel}<br>
        Predicted final grade: ${predictedGrade.toFixed(2)}<br>
        Grade delta: ${deltaLabel}
    `;

    renderManualRiskChart(riskProbability, riskLevel);
    renderManualGradeChart(predictedGrade, thresholds.average_grade, thresholds.median_grade);
}

function logisticScore(rawInput, model) {
    const standardized = rawInput.map((value, index) => (value - model.scaler_mean[index]) / model.scaler_scale[index]);
    const linearTerm = standardized.reduce(
        (sum, value, index) => sum + value * model.coefficients[index],
        model.intercept
    );
    return 1 / (1 + Math.exp(-linearTerm));
}

function linearScore(rawInput, model) {
    const standardized = rawInput.map((value, index) => (value - model.scaler_mean[index]) / model.scaler_scale[index]);
    return standardized.reduce(
        (sum, value, index) => sum + value * model.coefficients[index],
        model.intercept
    );
}

function renderManualRiskChart(riskProbability, riskLevel) {
    Plotly.newPlot("manualRiskChart", [
        {
            type: "bar",
            x: ["Risk probability"],
            y: [Number((riskProbability * 100).toFixed(2))],
            marker: {
                color: riskLevel === "high" ? "#c24f2a" : (riskLevel === "medium" ? "#d3a223" : "#0d7a5f")
            },
            hovertemplate: "%{y}%<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Probability (%)", range: [0, 100], gridcolor: "#e8e0d2" }
    }, { responsive: true, displayModeBar: false });
}

function renderManualGradeChart(predictedGrade, averageGrade, medianGrade) {
    Plotly.newPlot("manualGradeChart", [
        {
            type: "bar",
            x: ["Predicted grade", "Cohort average", "Cohort median"],
            y: [predictedGrade, averageGrade, medianGrade],
            marker: { color: ["#0d7a5f", "#64513c", "#c24f2a"] },
            hovertemplate: "%{x}: %{y:.2f}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 50, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Grade", gridcolor: "#e8e0d2" }
    }, { responsive: true, displayModeBar: false });
}

function bindFilters() {
    const search = document.getElementById("studentSearch");
    const riskFilter = document.getElementById("riskFilter");

    search.addEventListener("input", applyTableFilters);
    riskFilter.addEventListener("change", applyTableFilters);
}

function applyTableFilters() {
    const searchValue = document.getElementById("studentSearch").value.trim().toLowerCase();
    const riskFilter = document.getElementById("riskFilter").value;

    visibleStudents = (dashboardData.students || []).filter((student) => {
        const matchesSearch = student.user.toLowerCase().includes(searchValue);
        const matchesRisk = riskFilter === "all" || student.risk_level === riskFilter;
        return matchesSearch && matchesRisk;
    });

    renderStudentsTable(visibleStudents);
}

function renderStudentsTable(students) {
    const tbody = document.getElementById("studentsTableBody");
    tbody.innerHTML = "";

    for (const student of students) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${student.user}</td>
            <td><span class="risk-pill risk-${student.risk_level}">${titleCase(student.risk_level)}</span></td>
            <td>${formatPercent(student.risk_probability)}</td>
            <td>${student.predicted_outcome}</td>
            <td>${student.predicted_grade}</td>
            <td>${student.activity_score}</td>
            <td>${student.last_login}</td>
        `;
        tbody.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}

function formatPercent(value) {
    return `${(Number(value) * 100).toFixed(1)}%`;
}

function titleCase(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
}