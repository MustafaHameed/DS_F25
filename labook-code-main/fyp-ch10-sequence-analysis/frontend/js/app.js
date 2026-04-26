const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleSamples = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});

async function initializeDashboard() {
    setStatus("Loading sequence-analysis artifacts from outputs/backend/dashboard.json...");

    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        dashboardData = await response.json();
        visibleSamples = dashboardData.samples || [];

        renderMeta();
        renderOverview();
        renderValidationChart();
        renderClusterSizeChart();
        renderPrototypeList();
        renderActionCatalogue();
        populateFilters();
        bindFilters();
        bindManualDemo();
        renderSampleTable(visibleSamples);
        runManualSequenceAssignment();
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
    document.getElementById("totalSessions").textContent = overview.total_sessions;
    document.getElementById("uniqueStudents").textContent = overview.unique_students;
    document.getElementById("distinctActions").textContent = overview.distinct_actions;
    document.getElementById("chosenClusters").textContent = overview.chosen_clusters;
}

function renderValidationChart() {
    const metrics = dashboardData.validation_metrics || [];
    Plotly.newPlot("validationChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            x: metrics.map((item) => item.clusters),
            y: metrics.map((item) => item.silhouette),
            line: { color: "#2d6a4f", width: 3 },
            marker: { color: "#bc6c25", size: 10 },
            hovertemplate: "k=%{x}<br>Silhouette=%{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Clusters" },
        yaxis: { title: "Silhouette", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function renderClusterSizeChart() {
    const profiles = dashboardData.cluster_profiles || [];
    Plotly.newPlot("clusterSizeChart", [
        {
            type: "bar",
            x: profiles.map((item) => `Cluster ${item.cluster}`),
            y: profiles.map((item) => item.size),
            marker: { color: ["#2d6a4f", "#bc6c25", "#7c9a6d", "#8c5e34"] },
            hovertemplate: "%{x}: %{y} sessions<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Sessions", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function renderPrototypeList() {
    const container = document.getElementById("prototypeList");
    container.innerHTML = "";

    for (const profile of dashboardData.cluster_profiles || []) {
        const card = document.createElement("div");
        card.className = "prototype-card";
        card.innerHTML = `
            <strong>Cluster ${profile.cluster}</strong>
            Median length: ${Number(profile.median_length).toFixed(1)}<br>
            Top actions: ${profile.top_actions.join(", ")}<br>
            Prototype: ${profile.prototype_sequence.filter((value) => value !== "END").join(" -> ")}
        `;
        container.appendChild(card);
    }
}

function renderActionCatalogue() {
    const container = document.getElementById("actionCatalogue");
    container.innerHTML = "";

    for (const action of dashboardData.action_catalogue || []) {
        const chip = document.createElement("span");
        chip.className = "catalogue-chip";
        chip.textContent = action;
        container.appendChild(chip);
    }
}

function populateFilters() {
    const clusterFilter = document.getElementById("clusterFilter");
    for (const profile of dashboardData.cluster_profiles || []) {
        const option = document.createElement("option");
        option.value = String(profile.cluster);
        option.textContent = `Cluster ${profile.cluster}`;
        clusterFilter.appendChild(option);
    }
}

function bindFilters() {
    document.getElementById("sessionSearch").addEventListener("input", applyFilters);
    document.getElementById("clusterFilter").addEventListener("change", applyFilters);
}

function applyFilters() {
    const searchValue = document.getElementById("sessionSearch").value.trim().toLowerCase();
    const clusterValue = document.getElementById("clusterFilter").value;

    visibleSamples = (dashboardData.samples || []).filter((sample) => {
        const matchesSearch =
            sample.user.toLowerCase().includes(searchValue) ||
            sample.session_id.toLowerCase().includes(searchValue);
        const matchesCluster = clusterValue === "all" || String(sample.cluster) === clusterValue;
        return matchesSearch && matchesCluster;
    });

    renderSampleTable(visibleSamples);
}

function bindManualDemo() {
    const manualSequence = document.getElementById("manualSequence");
    manualSequence.value = dashboardData.manual_demo.default_sequence;

    document.getElementById("manualForm").addEventListener("submit", (event) => {
        event.preventDefault();
        runManualSequenceAssignment();
    });

    document.getElementById("resetSequence").addEventListener("click", () => {
        manualSequence.value = dashboardData.manual_demo.default_sequence;
        runManualSequenceAssignment();
    });
}

function runManualSequenceAssignment() {
    const rawValue = document.getElementById("manualSequence").value;
    const actions = rawValue
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
        .slice(0, dashboardData.manual_demo.max_sequence_length);

    const distances = (dashboardData.cluster_profiles || []).map((profile) => {
        const prototype = profile.prototype_sequence;
        const comparedLength = Math.max(actions.length, prototype.length);
        let mismatchCount = 0;

        for (let index = 0; index < comparedLength; index += 1) {
            const entered = actions[index] || "END";
            const reference = prototype[index] || "END";
            if (entered !== reference) {
                mismatchCount += 1;
            }
        }

        return {
            cluster: profile.cluster,
            distance: mismatchCount,
            prototype: prototype.filter((value) => value !== "END").join(" -> "),
            topActions: profile.top_actions.join(", "),
            medianLength: Number(profile.median_length).toFixed(1)
        };
    }).sort((left, right) => left.distance - right.distance);

    const bestMatch = distances[0];
    document.getElementById("manualSummary").innerHTML = `
        <strong>Closest match: Cluster ${bestMatch.cluster}</strong>
        Sequence length entered: ${actions.length}<br>
        Position mismatches vs prototype: ${bestMatch.distance}<br>
        Cluster median length: ${bestMatch.medianLength}<br>
        Cluster top actions: ${bestMatch.topActions}<br>
        Prototype path: ${bestMatch.prototype}
    `;

    Plotly.newPlot("manualDistanceChart", [
        {
            type: "bar",
            x: distances.map((item) => `Cluster ${item.cluster}`),
            y: distances.map((item) => item.distance),
            marker: {
                color: distances.map((item, index) => index === 0 ? "#2d6a4f" : "#d8cdbd")
            },
            hovertemplate: "%{x}: %{y} mismatches<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Mismatch Count", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function renderSampleTable(samples) {
    const body = document.getElementById("sampleTableBody");
    body.innerHTML = "";

    for (const sample of samples.slice(0, 180)) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${sample.user}</td>
            <td>${sample.session_id}</td>
            <td><span class="cluster-pill">Cluster ${sample.cluster}</span></td>
            <td>${sample.sequence_length}</td>
            <td>${sample.preview_sequence}</td>
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}