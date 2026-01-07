# Learning Analytics Dashboard - Frontend

A simplified web-based dashboard for visualizing student risk predictions from the Learning Analytics Prediction System.

## Features

- **Dashboard Overview**: Real-time stats on student risk distribution
- **Student Risk Analysis**: Sortable/filterable table of all students
- **Model Performance**: Charts showing prediction accuracy over time
- **Feature Analysis**: Interactive visualizations of feature importance and correlations

## File Structure

```
frontend/
├── index.html              # Main HTML structure
├── css/
│   └── styles.css         # Professional styling with blue theme
└── js/
    ├── app.js             # Application logic & navigation
    ├── charts.js          # Plotly.js chart generation
    └── sample_data.js     # Sample student prediction data
```

## Quick Start

1. **Open the dashboard**:
   ```
   Open `index.html` in your web browser
   ```

2. **Navigate between views**:
   - Click sidebar menu items to switch between Overview, Students, Predictions, and Features views

3. **Interact with data**:
   - Search/filter students in the Students view
   - Hover over charts for detailed information
   - Click "View" buttons to see student details

## Technology Stack

- **HTML5**: Semantic structure
- **CSS3**: Custom styling with CSS Grid and Flexbox
- **JavaScript (ES6)**: Modern vanilla JavaScript
- **Plotly.js**: Interactive charts and visualizations (loaded via CDN)

## Data Structure

The dashboard expects data in this format (see `sample_data.js`):

```javascript
{
    students: [
        {
            id: 'S001',
            name: 'Student Name',
            riskLevel: 'high|medium|low',
            probability: 0.85,
            activityScore: 32.5,
            lastLogin: '2026-01-06'
        },
        // ... more students
    ],
    predictions: {
        modelVersion: '2.0',
        accuracy: 0.89,
        // ... other metrics
    }
}
```

## Integrating Real Data

To connect to your Python prediction pipeline:

1. **Option A - CSV Integration**:
   - Add `PapaParse.js` library
   - Modify `app.js` to load CSV files from Python output
   - Parse prediction results into the expected format

2. **Option B - JSON Export**:
   - Export Python predictions as JSON
   - Replace `sample_data.js` with your JSON file

3. **Option C - REST API**:
   - Build a simple Flask/FastAPI backend
   - Fetch data using `fetch()` API in JavaScript

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

Requires modern browser with ES6 support.

## Future Enhancements

- Real-time data updates
- Export reports to PDF
- Individual student drill-down pages
- Email intervention alerts
- Custom date range filtering
- Model comparison views

## Color Scheme

- Primary Blue: `#0066cc`
- Success Green: `#27ae60`
- Warning Orange: `#f39c12`
- Danger Red: `#e74c3c`

## License

Part of the Learning Analytics Prediction System (Ch07) project.
