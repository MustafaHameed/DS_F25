const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleMembers = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});

async function initializeDashboard() {
    setStatus("Loading clustering outputs from outputs/backend/dashboard.json...");

    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        dashboardData = await response.json();
        visibleMembers = dashboardData.members || [];

        renderMeta();
        renderOverview();
        renderCharts();
        populateClusterControls();
        buildManualInputForm();
        renderMemberTable(visibleMembers);
        bindFilters();
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
    document.getElementById("totalNodes").textContent = overview.total_nodes;
    document.getElementById("featureCount").textContent = overview.feature_count;
    document.getElementById("chosenClusters").textContent = overview.chosen_clusters;
    document.getElementById("bestSilhouette").textContent = Number(overview.best_silhouette).toFixed(3);
}

function renderCharts() {
    renderClusterSizeChart();
    renderValidationChart();
    renderClusterProfileChart(Number(dashboardData.clusters[0]?.cluster || 1));
}

function renderClusterSizeChart() {
    const clusterSizes = dashboardData.cluster_sizes || [];
    Plotly.newPlot("clusterSizeChart", [
        {
            type: "bar",
            x: clusterSizes.map((item) => `Cluster ${item.cluster}`),
            y: clusterSizes.map((item) => item.count),
            marker: { color: ["#0b7c61", "#bd5b31", "#d8a332", "#4b6b88"] },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Nodes", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function renderValidationChart() {
    const metrics = dashboardData.validation_metrics || [];
    Plotly.newPlot("validationChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            name: "Silhouette",
            x: metrics.map((item) => item.k),
            y: metrics.map((item) => item.silhouette),
            line: { color: "#0b7c61", width: 3 }
        },
        {
            type: "scatter",
            mode: "lines+markers",
            name: "Davies-Bouldin",
            x: metrics.map((item) => item.k),
            y: metrics.map((item) => item.davies_bouldin),
            yaxis: "y2",
            line: { color: "#bd5b31", width: 3, dash: "dot" }
        }
    ], {
        margin: { t: 20, r: 50, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "k" },
        yaxis: { title: "Silhouette", gridcolor: "#e8dece" },
        yaxis2: { title: "Davies-Bouldin", overlaying: "y", side: "right" },
        legend: { orientation: "h" }
    }, { responsive: true, displayModeBar: false });
}

function renderClusterProfileChart(clusterId) {
    const profile = (dashboardData.cluster_profiles || []).find((item) => Number(item.cluster) === Number(clusterId));
    if (!profile) {
        return;
    }

    const featureColumns = dashboardData.feature_columns || [];
    Plotly.newPlot("clusterProfileChart", [
        {
            type: "bar",
            x: featureColumns.map(prettyName),
            y: featureColumns.map((column) => profile[column]),
            marker: { color: "#0b7c61" },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 90, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { tickangle: -35 },
        yaxis: { title: "Average Value", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function populateClusterControls() {
    const profileSelect = document.getElementById("clusterProfileSelect");
    const memberClusterFilter = document.getElementById("memberClusterFilter");
    profileSelect.innerHTML = "";

    for (const cluster of dashboardData.clusters || []) {
        const option = document.createElement("option");
        option.value = cluster.cluster;
        option.textContent = cluster.label;
        profileSelect.appendChild(option);

        const filterOption = document.createElement("option");
        filterOption.value = cluster.cluster;
        filterOption.textContent = cluster.label;
        memberClusterFilter.appendChild(filterOption);
    }

    profileSelect.addEventListener("change", (event) => {
        renderClusterProfileChart(Number(event.target.value));
    });
}

function buildManualInputForm() {
    const form = document.getElementById("manualInputForm");
    form.innerHTML = "";

    for (const field of dashboardData.field_schema || []) {
        const wrapper = document.createElement("div");
        wrapper.className = "input-field";
        wrapper.innerHTML = `
            <label for="field-${field.name}">${field.label}</label>
            <input id="field-${field.name}" name="${field.name}" type="number" step="${field.step}" min="${field.min}" max="${field.max}" value="${field.default}">
        `;
        form.appendChild(wrapper);
    }

    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Assign To Cluster";
    form.appendChild(submitButton);

    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.className = "secondary";
    resetButton.textContent = "Reset Defaults";
    resetButton.addEventListener("click", () => {
        for (const field of dashboardData.field_schema || []) {
            document.getElementById(`field-${field.name}`).value = field.default;
        }
        runManualAssignment();
    });
    form.appendChild(resetButton);

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        runManualAssignment();
    });
}

function runManualAssignment() {
    const featureOrder = dashboardData.scaler.feature_order;
    const means = dashboardData.scaler.mean;
    const scales = dashboardData.scaler.scale;

    const scaledInput = featureOrder.map((column, index) => {
        const value = Number(document.getElementById(`field-${column}`).value);
        return (value - means[index]) / scales[index];
    });

    const distances = (dashboardData.clusters || []).map((cluster) => {
        const centroid = featureOrder.map((column) => Number(cluster.centroid_scaled[column]));
        const distance = Math.sqrt(centroid.reduce((sum, value, index) => sum + ((scaledInput[index] - value) ** 2), 0));
        return { cluster: cluster.cluster, label: cluster.label, distance };
    }).sort((a, b) => a.distance - b.distance);

    const assigned = distances[0];
    const clusterInfo = dashboardData.clusters.find((cluster) => Number(cluster.cluster) === Number(assigned.cluster));
    document.getElementById("manualSummary").innerHTML = `
        <strong>${clusterInfo.label}</strong>
        Closest-cluster distance: ${assigned.distance.toFixed(3)}<br>
        Strongest signals: ${clusterInfo.top_high.join(", ")}<br>
        Lowest signals: ${clusterInfo.top_low.join(", ")}<br>
        Cluster size: ${clusterInfo.size} students
    `;

    Plotly.newPlot("manualDistanceChart", [
        {
            type: "bar",
            x: distances.map((item) => item.label),
            y: distances.map((item) => Number(item.distance.toFixed(4))),
            marker: {
                color: distances.map((item, index) => index === 0 ? "#0b7c61" : "#d8cfbd")
            },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 50, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Distance", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function bindFilters() {
    document.getElementById("memberSearch").addEventListener("input", applyMemberFilters);
    document.getElementById("memberClusterFilter").addEventListener("change", applyMemberFilters);
}

function applyMemberFilters() {
    const searchValue = document.getElementById("memberSearch").value.trim().toLowerCase();
    const clusterValue = document.getElementById("memberClusterFilter").value;
    visibleMembers = (dashboardData.members || []).filter((member) => {
        const matchesSearch = String(member.student_id).toLowerCase().includes(searchValue);
        const matchesCluster = clusterValue === "all" || String(member.cluster) === clusterValue;
        return matchesSearch && matchesCluster;
    });
    renderMemberTable(visibleMembers);
}

function renderMemberTable(members) {
    const featureColumns = dashboardData.feature_columns || [];
    const head = document.getElementById("memberTableHead");
    const body = document.getElementById("memberTableBody");

    head.innerHTML = `<tr><th>Student</th><th>Cluster</th>${featureColumns.slice(0, 4).map((column) => `<th>${prettyName(column)}</th>`).join("")}</tr>`;
    body.innerHTML = "";

    for (const member of members.slice(0, 160)) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${member.student_id}</td>
            <td><span class="cluster-pill">Cluster ${member.cluster}</span></td>
            ${featureColumns.slice(0, 4).map((column) => `<td>${Number(member[column]).toFixed(3)}</td>`).join("")}
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}

function prettyName(value) {
    return value.replace(/[_\.]/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}