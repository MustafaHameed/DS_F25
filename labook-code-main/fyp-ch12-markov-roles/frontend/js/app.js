const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleSamples = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});

async function initializeDashboard() {
    setStatus("Loading role-transition artifacts...");
    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        dashboardData = await response.json();
        visibleSamples = dashboardData.samples || [];

        renderMeta();
        renderOverview();
        renderClusterMetricChart();
        renderTransitionHeatmap();
        renderClusterSizeChart();
        renderGpaMixChart();
        renderClusterPrototypeList();
        bindManualDemo();
        bindFilters();
        renderSampleTable(visibleSamples);
        setStatus("Dashboard loaded from generated backend artifacts.");
    } catch (error) {
        console.error(error);
        setStatus("Backend output is missing. Run ./run/run_backend.ps1 and refresh this page.");
    }
}

function renderMeta() {
    document.getElementById("generatedAt").textContent = `Generated: ${dashboardData.project.generated_at}`;
}

function renderOverview() {
    const overview = dashboardData.overview;
    document.getElementById("totalLearners").textContent = overview.total_learners;
    document.getElementById("sequenceLength").textContent = overview.sequence_length;
    document.getElementById("roleStates").textContent = overview.role_states;
    document.getElementById("chosenClusters").textContent = overview.chosen_clusters;
}

function renderClusterMetricChart() {
    const metrics = dashboardData.cluster_metrics || [];
    Plotly.newPlot("clusterMetricChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            name: "BIC",
            x: metrics.map((item) => item.clusters),
            y: metrics.map((item) => item.bic),
            line: { color: "#1c6a62", width: 3 }
        },
        {
            type: "bar",
            name: "Silhouette",
            x: metrics.map((item) => item.clusters),
            y: metrics.map((item) => item.silhouette),
            marker: { color: "rgba(168,79,44,0.35)" },
            yaxis: "y2"
        }
    ], {
        margin: { t: 20, r: 30, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Clusters" },
        yaxis: { title: "BIC", gridcolor: "#eadfcd" },
        yaxis2: { title: "Silhouette", overlaying: "y", side: "right" },
        legend: { orientation: "h" }
    }, { responsive: true, displayModeBar: false });
}

function renderTransitionHeatmap() {
    const roles = dashboardData.role_states || [];
    const matrix = dashboardData.overall_transition || {};
    Plotly.newPlot("transitionHeatmap", [
        {
            type: "heatmap",
            x: roles,
            y: roles,
            z: roles.map((source) => roles.map((target) => Number(matrix[source]?.[target] || 0))),
            colorscale: [[0, "#f6e6dc"], [1, "#1c6a62"]],
            hovertemplate: "%{y} -> %{x}: %{z:.2f}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 70 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)"
    }, { responsive: true, displayModeBar: false });
}

function renderClusterSizeChart() {
    const profiles = dashboardData.cluster_profiles || [];
    Plotly.newPlot("clusterSizeChart", [
        {
            type: "bar",
            x: profiles.map((item) => item.cluster_label),
            y: profiles.map((item) => item.size),
            marker: { color: "#1c6a62" },
            hovertemplate: "%{x}: %{y} learners<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 60, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Learners", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderGpaMixChart() {
    const profiles = dashboardData.cluster_profiles || [];
    const levels = ["Low", "Middle", "High"];
    Plotly.newPlot("gpaMixChart", levels.map((level, index) => ({
        type: "bar",
        name: level,
        x: profiles.map((item) => item.cluster_label),
        y: profiles.map((item) => item.gpa_distribution[level] || 0),
        marker: { color: ["#a84f2c", "#d7b24c", "#1c6a62"][index] }
    })), {
        barmode: "stack",
        margin: { t: 20, r: 20, b: 60, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Proportion", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderClusterPrototypeList() {
    const container = document.getElementById("clusterPrototypeList");
    container.innerHTML = "";
    for (const profile of dashboardData.cluster_profiles || []) {
        const card = document.createElement("div");
        card.className = "prototype-card";
        card.innerHTML = `
            <strong>${profile.cluster_label}</strong>
            Learners: ${profile.size}<br>
            Dominant roles: ${profile.dominant_roles.join(", ")}<br>
            Prototype: ${profile.prototype_sequence.join(" -> ")}
        `;
        container.appendChild(card);
    }
}

function bindManualDemo() {
    const textarea = document.getElementById("manualSequence");
    textarea.value = (dashboardData.manual_demo.default_sequence || []).join(", ");
    document.getElementById("assignButton").addEventListener("click", runManualAssignment);
    document.getElementById("resetButton").addEventListener("click", () => {
        textarea.value = (dashboardData.manual_demo.default_sequence || []).join(", ");
        runManualAssignment();
    });
    runManualAssignment();
}

function runManualAssignment() {
    const textarea = document.getElementById("manualSequence");
    const allowedRoles = dashboardData.manual_demo.allowed_roles || [];
    const tokens = textarea.value.split(",").map((token) => token.trim()).filter(Boolean);

    if (!tokens.length) {
        document.getElementById("manualSummary").innerHTML = "Enter a comma-separated role sequence first.";
        return;
    }

    const invalid = tokens.filter((token) => !allowedRoles.includes(token));
    if (invalid.length) {
        document.getElementById("manualSummary").innerHTML = `Invalid roles detected: ${invalid.join(", ")}`;
        return;
    }

    const models = dashboardData.manual_demo.cluster_models || {};
    const scores = Object.entries(models).map(([label, model]) => {
        const prototype = model.prototype_sequence || [];
        let mismatches = 0;
        tokens.forEach((role, index) => {
            if (prototype[index] && role !== prototype[index]) {
                mismatches += 1;
            }
        });
        return {
            label,
            mismatches,
            dominantRoles: model.dominant_roles.join(", "),
            prototype: prototype.join(" -> ")
        };
    }).sort((left, right) => left.mismatches - right.mismatches);

    const best = scores[0];
    document.getElementById("manualSummary").innerHTML = `
        <strong>${best.label}</strong>
        Position mismatches: ${best.mismatches}<br>
        Dominant roles: ${best.dominantRoles}<br>
        Prototype path: ${best.prototype}
    `;

    Plotly.newPlot("manualClusterChart", [{
        type: "bar",
        x: scores.map((item) => item.label),
        y: scores.map((item) => item.mismatches),
        marker: { color: scores.map((item, index) => index === 0 ? "#1c6a62" : "#d9cfbf") },
        hovertemplate: "%{x}: %{y} mismatches<extra></extra>"
    }], {
        margin: { t: 20, r: 20, b: 60, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Mismatch Count", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function bindFilters() {
    document.getElementById("sampleSearch").addEventListener("input", () => {
        const query = document.getElementById("sampleSearch").value.trim().toLowerCase();
        visibleSamples = (dashboardData.samples || []).filter((sample) => (
            String(sample.ID).toLowerCase().includes(query) ||
            String(sample.GPA).toLowerCase().includes(query)
        ));
        renderSampleTable(visibleSamples);
    });
}

function renderSampleTable(samples) {
    const body = document.getElementById("sampleTableBody");
    body.innerHTML = "";
    for (const sample of samples.slice(0, 160)) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${sample.ID}</td>
            <td>${sample.GPA}</td>
            <td><span class="cluster-pill">${sample.cluster_label}</span></td>
            <td>${sample.sequence_preview}</td>
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}