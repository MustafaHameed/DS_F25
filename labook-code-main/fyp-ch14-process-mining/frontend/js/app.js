const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleSamples = [];

document.addEventListener("DOMContentLoaded", () => initializeDashboard());

async function initializeDashboard() {
    setStatus("Loading process-mining dashboard artifacts...");
    try {
        const response = await fetch(DASHBOARD_URL, { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        dashboardData = await response.json();
        visibleSamples = dashboardData.samples || [];

        renderMeta();
        renderOverview();
        renderActivityFrequency();
        renderGroupFrequency();
        renderProcessSankey();
        renderGroupTransitions();
        renderActionCatalogue();
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
    document.getElementById("totalEvents").textContent = overview.total_events;
    document.getElementById("trimmedEvents").textContent = overview.trimmed_events;
    document.getElementById("totalSessions").textContent = overview.total_sessions;
    document.getElementById("distinctActions").textContent = overview.distinct_actions;
}

function renderActivityFrequency() {
    const rows = dashboardData.activity_frequency || [];
    Plotly.newPlot("activityFrequencyChart", [{
        type: "bar",
        x: rows.map((item) => item.Action),
        y: rows.map((item) => item.proportion),
        marker: { color: "#1b6b73" },
        hovertemplate: "%{x}: %{y:.2%}<extra></extra>"
    }], {
        margin: { t: 20, r: 20, b: 80, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Proportion", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderGroupFrequency() {
    const rows = dashboardData.activity_frequency_by_group || [];
    const groups = [...new Set(rows.map((item) => item.AchievingGroup))];
    const topActions = [...new Set(rows.slice(0, 12).map((item) => item.Action))];

    Plotly.newPlot("groupFrequencyChart", groups.map((group, index) => ({
        type: "bar",
        name: group,
        x: topActions,
        y: topActions.map((action) => {
            const match = rows.find((item) => item.AchievingGroup === group && item.Action === action);
            return match ? match.proportion : 0;
        }),
        marker: { color: ["#1b6b73", "#bf5b31"][index] }
    })), {
        barmode: "group",
        margin: { t: 20, r: 20, b: 90, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Proportion", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function renderProcessSankey() {
    const transitions = dashboardData.top_transitions || [];
    const labels = [...new Set(transitions.flatMap((item) => [item.Action, item.next_action]))];
    const labelIndex = new Map(labels.map((label, index) => [label, index]));

    Plotly.newPlot("processSankey", [{
        type: "sankey",
        arrangement: "snap",
        node: {
            label: labels,
            color: labels.map(() => "rgba(27,107,115,0.7)")
        },
        link: {
            source: transitions.map((item) => labelIndex.get(item.Action)),
            target: transitions.map((item) => labelIndex.get(item.next_action)),
            value: transitions.map((item) => item.count),
            color: transitions.map(() => "rgba(191,91,49,0.25)")
        }
    }], {
        margin: { t: 10, r: 10, b: 10, l: 10 },
        paper_bgcolor: "rgba(0,0,0,0)"
    }, { responsive: true, displayModeBar: false });
}

function renderGroupTransitions() {
    const groups = Object.keys(dashboardData.group_top_transitions || {});
    const topLabels = [];
    for (const group of groups) {
        for (const item of (dashboardData.group_top_transitions[group] || []).slice(0, 5)) {
            const label = `${item.Action} -> ${item.next_action}`;
            if (!topLabels.includes(label)) {
                topLabels.push(label);
            }
        }
    }

    Plotly.newPlot("groupTransitionChart", groups.map((group, index) => ({
        type: "bar",
        name: group,
        x: topLabels,
        y: topLabels.map((label) => {
            const match = (dashboardData.group_top_transitions[group] || []).find((item) => `${item.Action} -> ${item.next_action}` === label);
            return match ? match.count : 0;
        }),
        marker: { color: ["#1b6b73", "#bf5b31"][index] }
    })), {
        barmode: "group",
        margin: { t: 20, r: 20, b: 110, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Transition count", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
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

function bindManualDemo() {
    const textarea = document.getElementById("manualPath");
    textarea.value = (dashboardData.manual_demo.default_path || []).join(", ");
    document.getElementById("scoreButton").addEventListener("click", runManualScore);
    document.getElementById("resetButton").addEventListener("click", () => {
        textarea.value = (dashboardData.manual_demo.default_path || []).join(", ");
        runManualScore();
    });
    runManualScore();
}

function runManualScore() {
    const tokens = document.getElementById("manualPath").value.split(",").map((token) => token.trim()).filter(Boolean);
    const invalid = tokens.filter((token) => !dashboardData.action_catalogue.includes(token));
    if (!tokens.length) {
        document.getElementById("manualSummary").innerHTML = "Enter a comma-separated action path first.";
        return;
    }
    if (invalid.length) {
        document.getElementById("manualSummary").innerHTML = `Invalid actions detected: ${invalid.join(", ")}`;
        return;
    }

    const scores = Object.entries(dashboardData.manual_demo.group_models || {}).map(([group, model]) => {
        let logLikelihood = Math.log(model.initial_probs[tokens[0]] || 1e-9);
        for (let index = 0; index < tokens.length - 1; index += 1) {
            const source = tokens[index];
            const target = tokens[index + 1];
            const probability = model.transition_probs[source]?.[target] || 1e-9;
            logLikelihood += Math.log(probability);
        }
        return { group, logLikelihood };
    }).sort((left, right) => right.logLikelihood - left.logLikelihood);

    const best = scores[0];
    const second = scores[1];
    document.getElementById("manualSummary").innerHTML = `
        <strong>${best.group}</strong>
        Log-likelihood: ${best.logLikelihood.toFixed(2)}<br>
        Margin over alternative: ${(best.logLikelihood - second.logLikelihood).toFixed(2)}<br>
        Path length: ${tokens.length}
    `;

    Plotly.newPlot("manualLikelihoodChart", [{
        type: "bar",
        x: scores.map((item) => item.group),
        y: scores.map((item) => item.logLikelihood),
        marker: { color: scores.map((item, index) => index === 0 ? "#1b6b73" : "#bf5b31") },
        hovertemplate: "%{x}: %{y:.2f}<extra></extra>"
    }], {
        margin: { t: 20, r: 20, b: 60, l: 45 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Log-likelihood", gridcolor: "#eadfcd" }
    }, { responsive: true, displayModeBar: false });
}

function bindFilters() {
    document.getElementById("sampleSearch").addEventListener("input", () => {
        const query = document.getElementById("sampleSearch").value.trim().toLowerCase();
        visibleSamples = (dashboardData.samples || []).filter((sample) => (
            String(sample.user).toLowerCase().includes(query) ||
            String(sample.AchievingGroup).toLowerCase().includes(query)
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
            <td>${sample.session_id}</td>
            <td>${sample.user}</td>
            <td><span class="group-pill">${sample.AchievingGroup}</span></td>
            <td>${sample.event_count}</td>
            <td>${sample.action_path}</td>
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}