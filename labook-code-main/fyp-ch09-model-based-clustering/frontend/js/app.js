const DASHBOARD_URL = "../outputs/backend/dashboard.json";

let dashboardData = null;
let visibleMembers = [];

document.addEventListener("DOMContentLoaded", () => {
    initializeDashboard();
});

async function initializeDashboard() {
    setStatus("Loading profile outputs from outputs/backend/dashboard.json...");

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
        populateControls();
        buildManualInputForm();
        renderMemberTable(visibleMembers);
        bindFilters();
        runManualProfileEstimate();
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
    document.getElementById("totalStudents").textContent = overview.total_students;
    document.getElementById("chosenProfiles").textContent = overview.chosen_profiles;
    document.getElementById("avgPosterior").textContent = `${(overview.avg_assignment_probability * 100).toFixed(1)}%`;
    document.getElementById("avgEntropy").textContent = Number(overview.avg_entropy).toFixed(3);
}

function renderCharts() {
    renderModelSelectionChart();
    renderProfileSizeChart();
    renderProfileMeanChart(Number(dashboardData.profiles[0]?.profile || 1));
}

function renderModelSelectionChart() {
    const metrics = dashboardData.model_selection || [];
    Plotly.newPlot("modelSelectionChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            name: "BIC",
            x: metrics.map((item) => item.components),
            y: metrics.map((item) => item.bic),
            line: { color: "#165a8c", width: 3 }
        },
        {
            type: "scatter",
            mode: "lines+markers",
            name: "AIC",
            x: metrics.map((item) => item.components),
            y: metrics.map((item) => item.aic),
            line: { color: "#ab5f2f", width: 3, dash: "dot" }
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 50 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        xaxis: { title: "Components" },
        yaxis: { title: "Criterion", gridcolor: "#e8dece" },
        legend: { orientation: "h" }
    }, { responsive: true, displayModeBar: false });
}

function renderProfileSizeChart() {
    const profileSizes = dashboardData.profile_sizes || [];
    Plotly.newPlot("profileSizeChart", [
        {
            type: "bar",
            x: profileSizes.map((item) => `Profile ${item.profile}`),
            y: profileSizes.map((item) => item.count),
            marker: { color: ["#165a8c", "#ab5f2f", "#d5a53f", "#3f6b66"] },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 40, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Students", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function renderProfileMeanChart(profileId) {
    const profile = (dashboardData.profile_means || []).find((item) => Number(item.profile) === Number(profileId));
    if (!profile) {
        return;
    }

    const featureColumns = dashboardData.feature_columns || [];
    Plotly.newPlot("profileMeanChart", [
        {
            type: "scatter",
            mode: "lines+markers",
            x: featureColumns,
            y: featureColumns.map((column) => profile[column]),
            line: { color: "#165a8c", width: 3 },
            marker: { size: 10, color: "#ab5f2f" },
            hovertemplate: "%{x}: %{y}<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 50, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Average Score", gridcolor: "#e8dece" }
    }, { responsive: true, displayModeBar: false });
}

function populateControls() {
    const profileSelect = document.getElementById("profileSelect");
    const profileFilter = document.getElementById("profileFilter");
    profileSelect.innerHTML = "";

    for (const profile of dashboardData.profiles || []) {
        const option = document.createElement("option");
        option.value = profile.profile;
        option.textContent = profile.label;
        profileSelect.appendChild(option);

        const filterOption = document.createElement("option");
        filterOption.value = profile.profile;
        filterOption.textContent = profile.label;
        profileFilter.appendChild(filterOption);
    }

    profileSelect.addEventListener("change", (event) => {
        renderProfileMeanChart(Number(event.target.value));
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
    submitButton.textContent = "Estimate Profile";
    form.appendChild(submitButton);

    const resetButton = document.createElement("button");
    resetButton.type = "button";
    resetButton.className = "secondary";
    resetButton.textContent = "Reset Defaults";
    resetButton.addEventListener("click", () => {
        for (const field of dashboardData.field_schema || []) {
            document.getElementById(`field-${field.name}`).value = field.default;
        }
        runManualProfileEstimate();
    });
    form.appendChild(resetButton);

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        runManualProfileEstimate();
    });
}

function runManualProfileEstimate() {
    const featureOrder = dashboardData.scaler.feature_order;
    const scaledInput = featureOrder.map((column, index) => {
        const value = Number(document.getElementById(`field-${column}`).value);
        return (value - dashboardData.scaler.mean[index]) / dashboardData.scaler.scale[index];
    });

    const logScores = dashboardData.gmm.weights.map((weight, componentIndex) => {
        let logDensity = Math.log(weight);
        for (let featureIndex = 0; featureIndex < featureOrder.length; featureIndex += 1) {
            const variance = dashboardData.gmm.variances[componentIndex][featureIndex];
            const mean = dashboardData.gmm.means[componentIndex][featureIndex];
            const delta = scaledInput[featureIndex] - mean;
            logDensity += -0.5 * (Math.log(2 * Math.PI * variance) + ((delta ** 2) / variance));
        }
        return logDensity;
    });

    const maxLog = Math.max(...logScores);
    const expScores = logScores.map((score) => Math.exp(score - maxLog));
    const total = expScores.reduce((sum, value) => sum + value, 0);
    const probabilities = expScores.map((value) => value / total);
    const entropy = -probabilities.reduce((sum, probability) => sum + probability * Math.log(probability + 1e-12), 0);

    const probabilityRows = probabilities.map((probability, index) => ({
        profile: index + 1,
        label: `Profile ${index + 1}`,
        probability
    })).sort((a, b) => b.probability - a.probability);

    const assigned = probabilityRows[0];
    const profileInfo = dashboardData.profiles.find((profile) => Number(profile.profile) === Number(assigned.profile));
    document.getElementById("manualSummary").innerHTML = `
        <strong>${profileInfo.label}</strong>
        Posterior probability: ${(assigned.probability * 100).toFixed(1)}%<br>
        Mean profile signals: ${profileInfo.top_high.join(", ")}<br>
        Lowest relative signal: ${profileInfo.top_low.join(", ")}<br>
        Input entropy: ${entropy.toFixed(3)}
    `;

    Plotly.newPlot("manualProbabilityChart", [
        {
            type: "bar",
            x: probabilityRows.map((item) => item.label),
            y: probabilityRows.map((item) => Number((item.probability * 100).toFixed(2))),
            marker: {
                color: probabilityRows.map((item, index) => index === 0 ? "#165a8c" : "#d9cfbf")
            },
            hovertemplate: "%{x}: %{y}%<extra></extra>"
        }
    ], {
        margin: { t: 20, r: 20, b: 50, l: 40 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        yaxis: { title: "Probability (%)", gridcolor: "#e8dece", range: [0, 100] }
    }, { responsive: true, displayModeBar: false });
}

function bindFilters() {
    document.getElementById("memberSearch").addEventListener("input", applyFilters);
    document.getElementById("profileFilter").addEventListener("change", applyFilters);
}

function applyFilters() {
    const searchValue = document.getElementById("memberSearch").value.trim().toLowerCase();
    const profileValue = document.getElementById("profileFilter").value;
    visibleMembers = (dashboardData.members || []).filter((member) => {
        const matchesSearch = String(member.student_id).toLowerCase().includes(searchValue);
        const matchesProfile = profileValue === "all" || String(member.profile) === profileValue;
        return matchesSearch && matchesProfile;
    });
    renderMemberTable(visibleMembers);
}

function renderMemberTable(members) {
    const body = document.getElementById("memberTableBody");
    body.innerHTML = "";

    for (const member of members.slice(0, 180)) {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${member.student_id}</td>
            <td><span class="profile-pill">Profile ${member.profile}</span></td>
            <td>${Number(member.BehvEngmnt).toFixed(3)}</td>
            <td>${Number(member.CognEngmnt).toFixed(3)}</td>
            <td>${Number(member.EmotEngmnt).toFixed(3)}</td>
            <td>${(Number(member.AssignmentProbability) * 100).toFixed(1)}%</td>
            <td>${Number(member.Entropy).toFixed(3)}</td>
        `;
        body.appendChild(row);
    }
}

function setStatus(message) {
    document.getElementById("statusMessage").textContent = message;
}