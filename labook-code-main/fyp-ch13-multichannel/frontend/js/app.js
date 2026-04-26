const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleSamples = [];

document.addEventListener("DOMContentLoaded", () => initializeDashboard());

async function initializeDashboard() {
    setStatus("Loading multichannel dashboard artifacts...");
    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        dashboardData = await response.json();
        visibleSamples = dashboardData.samples || [];

        renderMeta();
        renderOverview();
        renderDistributionChart("engagementChart", dashboardData.engagement_distribution, "Engagement", dashboardData.engagement_states, ["#2aa746", "#f0c93b", "#d8435f"]);
        renderDistributionChart("achievementChart", dashboardData.achievement_distribution, "Achievement", dashboardData.achievement_states, ["#2c5ac5", "#58a8ff", "#9fe0ff"]);
        renderClusterValidation();
        renderClusterGradeChart();
        renderPrototypeList();
        buildManualForm();
        bindFilters();
        renderSampleTable(visibleSamples);
        runManualAssignment();
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
    document.getElementById("totalRecords").textContent = overview.total_records;
    document.getElementById("uniqueStudents").textContent = overview.unique_students;
    document.getElementById("sequenceLength").textContent = overview.sequence_length;
    document.getElementById("chosenClusters").textContent = overview.chosen_clusters;
}

function renderDistributionChart(targetId, rows, dimension, states, colors) {
    const traces = states.map((state, index) => ({
        type: "bar",
        name: state,
        x: [...new Set(rows.map((item) => item.Sequence))],
        y: [...new Set(rows.map((item) => item.Sequence))].map((step) => {
            const match = rows.find((item) => item.Sequence === step && item[dimension] === state);
            return match ? match.proportion : 0;
        }),
        marker: { color: colors[index] }
    }));

    Plotly.newPlot(targetId, traces, {
        barmode: "stack",
        margin: { t: 20, r: 20, b: 45, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Sequence Position" },
        yaxis: { title: "Proportion", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderClusterValidation() {
    const rows = dashboardData.cluster_validation || [];
    Plotly.newPlot("clusterValidationChart", [{
        type: "scatter",
        mode: "lines+markers",
        x: rows.map((item) => item.clusters),
        y: rows.map((item) => item.silhouette),
        line: { color: "#225f96", width: 3 },
        marker: { color: "#bb5e36", size: 10 }
    }], {
        margin: { t: 20, r: 20, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Clusters" },
        yaxis: { title: "Silhouette", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderClusterGradeChart() {
    const rows = dashboardData.cluster_profiles || [];
    Plotly.newPlot("clusterGradeChart", [{
        type: "bar",
        x: rows.map((item) => item.cluster_label),
        y: rows.map((item) => item.mean_final_grade),
        marker: { color: "#225f96" },
        hovertemplate: "%{x}: %{y:.2f}<extra></extra>"
    }], {
        margin: { t: 20, r: 20, b: 60, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Mean final grade", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderPrototypeList() {
    const container = document.getElementById("prototypeList");
    container.innerHTML = "";
    for (const profile of dashboardData.cluster_profiles || []) {
        const card = document.createElement("div");
        card.className = "prototype-card";
        card.innerHTML = `
            <strong>${profile.cluster_label}</strong>
            Students: ${profile.size}<br>
            Mean final grade: ${profile.mean_final_grade}<br>
            Engagement: ${profile.prototype_engagement.join(" -> ")}<br>
            Achievement: ${profile.prototype_achievement.join(" -> ")}<br>
            Signature states: ${profile.dominant_combined_states.join(", ")}
        `;
        container.appendChild(card);
    }
}

function buildManualForm() {
    const form = document.getElementById("manualForm");
    form.innerHTML = "";

    for (const field of dashboardData.manual_demo.field_schema || []) {
        const row = document.createElement("div");
        row.className = "input-row";
        row.innerHTML = `
            <label>Step ${field.step} Engagement</label>
            <label>Step ${field.step} Achievement</label>
        `;

        const engagementSelect = document.createElement("select");
        engagementSelect.id = `engagement-${field.step}`;
        for (const state of dashboardData.engagement_states || []) {
            const option = document.createElement("option");
            option.value = state;
            option.textContent = state;
            option.selected = state === field.default_engagement;
            engagementSelect.appendChild(option);
        }

        const achievementSelect = document.createElement("select");
        achievementSelect.id = `achievement-${field.step}`;
        for (const state of dashboardData.achievement_states || []) {
            const option = document.createElement("option");
            option.value = state;
            option.textContent = state;
            option.selected = state === field.default_achievement;
            achievementSelect.appendChild(option);
        }

        row.children[0].appendChild(engagementSelect);
        row.children[1].appendChild(achievementSelect);
        form.appendChild(row);
    }

    const actions = document.createElement("div");
    actions.className = "form-actions";
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Estimate Cluster";
    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.className = "secondary";
    resetButton.textContent = "Reset Defaults";
    resetButton.addEventListener("click", () => {
        for (const field of dashboardData.manual_demo.field_schema || []) {
            document.getElementById(`engagement-${field.step}`).value = field.default_engagement;
            document.getElementById(`achievement-${field.step}`).value = field.default_achievement;
        }
        runManualAssignment();
    });
    actions.appendChild(submitButton);
    actions.appendChild(resetButton);
    form.appendChild(actions);

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        runManualAssignment();
    });
}

function runManualAssignment() {
    const positions = dashboardData.manual_demo.field_schema || [];
    const manualPairs = positions.map((field) => ({
        engagement: document.getElementById(`engagement-${field.step}`).value,
        achievement: document.getElementById(`achievement-${field.step}`).value
    }));

    const scores = Object.entries(dashboardData.manual_demo.profiles || {}).map(([label, profile]) => {
        let mismatches = 0;
        manualPairs.forEach((pair, index) => {
            if (pair.engagement !== profile.prototype_engagement[index]) {
                mismatches += 1;
            }
            if (pair.achievement !== profile.prototype_achievement[index]) {
                mismatches += 1;
            }
        });
        return {
            label,
            mismatches,
            dominantStates: profile.dominant_combined_states.join(", "),
            meanFinalGrade: profile.mean_final_grade,
            engagementPath: profile.prototype_engagement.join(" -> "),
            achievementPath: profile.prototype_achievement.join(" -> ")
        };
    }).sort((left, right) => left.mismatches - right.mismatches);

    const best = scores[0];
    document.getElementById("manualSummary").innerHTML = `
        <strong>${best.label}</strong>
        Pairwise mismatches: ${best.mismatches}<br>
        Mean final grade: ${best.meanFinalGrade}<br>
        Signature states: ${best.dominantStates}<br>
        Engagement path: ${best.engagementPath}<br>
        Achievement path: ${best.achievementPath}
    `;

    Plotly.newPlot("manualClusterChart", [{
        type: "bar",
        x: scores.map((item) => item.label),
        y: scores.map((item) => item.mismatches),
        marker: { color: scores.map((item, index) => index === 0 ? "#225f96" : "#d8cfbf") },
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
            String(sample.UserID).toLowerCase().includes(query) ||
            String(sample.cluster_label).toLowerCase().includes(query)
        ));
        renderSampleTable(visibleSamples);
    });
}

function renderSampleTable(samples) {
    const body = document.getElementById("sampleTableBody");
    body.innerHTML = "";
    for (const sample of samples.slice(0, 180)) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${sample.UserID}</td>
            <td><span class="cluster-pill">${sample.cluster_label}</span></td>
            <td>${Number(sample.Final_Grade).toFixed(2)}</td>
            <td>${sample.multichannel_path}</td>
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}