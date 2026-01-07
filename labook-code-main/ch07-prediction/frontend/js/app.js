/**
 * Learning Analytics Dashboard - Main Application Logic
 */

// Global state
let currentView = 'overview';
let studentsData = [];
let predictionsData = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    setupNavigation();
    loadData();
    updateLastUpdateTime();
    
    console.log('Dashboard initialized successfully');
}

/**
 * Setup navigation handlers
 */
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const viewName = this.getAttribute('data-view');
            switchView(viewName);
        });
    });
}

/**
 * Switch between different views
 */
function switchView(viewName) {
    // Update navigation active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-view="${viewName}"]`).classList.add('active');
    
    // Update views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });
    document.getElementById(`${viewName}-view`).classList.add('active');
    
    // Update header title
    const titles = {
        'overview': 'Dashboard Overview',
        'students': 'Student Risk Analysis',
        'predictions': 'Model Predictions & Performance',
        'features': 'Feature Analysis'
    };
    document.getElementById('viewTitle').textContent = titles[viewName];
    
    currentView = viewName;
    
    // Load view-specific content
    loadViewContent(viewName);
}

/**
 * Load data from sample or API
 */
function loadData() {
    // Using sample data for now
    if (typeof SAMPLE_DATA !== 'undefined') {
        studentsData = SAMPLE_DATA.students;
        predictionsData = SAMPLE_DATA.predictions;
        
        updateStatCards();
        loadViewContent('overview');
    } else {
        console.error('Sample data not loaded');
    }
}

/**
 * Update statistic cards
 */
function updateStatCards() {
    const totalStudents = studentsData.length;
    const highRisk = studentsData.filter(s => s.riskLevel === 'high').length;
    const mediumRisk = studentsData.filter(s => s.riskLevel === 'medium').length;
    const lowRisk = studentsData.filter(s => s.riskLevel === 'low').length;
    
    document.getElementById('totalStudents').textContent = totalStudents;
    document.getElementById('highRisk').textContent = highRisk;
    document.getElementById('mediumRisk').textContent = mediumRisk;
    document.getElementById('lowRisk').textContent = lowRisk;
}

/**
 * Load content specific to each view
 */
function loadViewContent(viewName) {
    switch(viewName) {
        case 'overview':
            createRiskTimelineChart();
            createActivityHeatmap();
            break;
        case 'students':
            populateStudentsTable();
            setupTableFilters();
            break;
        case 'predictions':
            createModelPerformanceChart();
            createPredictionDistribution();
            createConfusionMatrix();
            break;
        case 'features':
            createFeatureImportanceChart();
            createCorrelationMatrix();
            createFeatureDistributions();
            break;
    }
}

/**
 * Populate students table
 */
function populateStudentsTable() {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';
    
    studentsData.forEach(student => {
        const row = createStudentRow(student);
        tbody.appendChild(row);
    });
}

/**
 * Create a student table row
 */
function createStudentRow(student) {
    const tr = document.createElement('tr');
    
    const riskClass = `risk-${student.riskLevel}`;
    const riskText = student.riskLevel.charAt(0).toUpperCase() + student.riskLevel.slice(1);
    
    tr.innerHTML = `
        <td>${student.id}</td>
        <td>${student.name}</td>
        <td><span class="risk-badge ${riskClass}">${riskText}</span></td>
        <td>${(student.probability * 100).toFixed(1)}%</td>
        <td>${student.activityScore.toFixed(1)}</td>
        <td>${student.lastLogin}</td>
        <td><button class="action-btn" onclick="viewStudentDetail('${student.id}')">View</button></td>
    `;
    
    return tr;
}

/**
 * Setup table filters
 */
function setupTableFilters() {
    const searchInput = document.getElementById('searchStudent');
    const riskFilter = document.getElementById('riskFilter');
    
    searchInput.addEventListener('input', filterTable);
    riskFilter.addEventListener('change', filterTable);
}

/**
 * Filter students table
 */
function filterTable() {
    const searchTerm = document.getElementById('searchStudent').value.toLowerCase();
    const riskLevel = document.getElementById('riskFilter').value;
    
    const rows = document.querySelectorAll('#studentsTableBody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matchesSearch = text.includes(searchTerm);
        const studentRisk = row.querySelector('.risk-badge').textContent.toLowerCase();
        const matchesRisk = riskLevel === 'all' || studentRisk === riskLevel;
        
        row.style.display = (matchesSearch && matchesRisk) ? '' : 'none';
    });
}

/**
 * View student detail (placeholder)
 */
function viewStudentDetail(studentId) {
    const student = studentsData.find(s => s.id === studentId);
    if (student) {
        alert(`Student Details:\n\nID: ${student.id}\nName: ${student.name}\nRisk: ${student.riskLevel}\nProbability: ${(student.probability * 100).toFixed(1)}%\nActivity Score: ${student.activityScore.toFixed(1)}`);
    }
}

/**
 * Refresh data
 */
function refreshData() {
    console.log('Refreshing data...');
    loadData();
    updateLastUpdateTime();
    
    // Show feedback
    const btn = event.target;
    btn.textContent = '✓ Refreshed';
    setTimeout(() => {
        btn.textContent = '🔄 Refresh';
    }, 2000);
}

/**
 * Export report (placeholder)
 */
function exportReport() {
    console.log('Exporting report...');
    alert('Export functionality will generate a PDF report with current analytics data.');
}

/**
 * Update last update timestamp
 */
function updateLastUpdateTime() {
    const now = new Date();
    const timeStr = now.toLocaleString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    document.getElementById('lastUpdate').textContent = timeStr;
}
