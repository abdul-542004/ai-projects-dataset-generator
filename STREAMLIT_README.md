# AI Projects Dataset - Interactive Streamlit Dashboard

This interactive Streamlit dashboard provides comprehensive analysis of the synthetic AI projects dataset containing 500 evidence-based project profiles designed for composite case studies.

## Features

### 🤖 Interactive Analysis Dashboard
- **Overview Tab**: Dataset validation, key metrics, and research benchmarks
- **Company Demographics**: Firmographic analysis with interactive filters
- **AI Projects**: Project characteristics, complexity, and success patterns
- **Business Impact**: Revenue, EBITDA, ROI, and payback analysis
- **Correlations**: Evidence-based correlations including MIT J-curve
- **Insights**: Key findings and recommendations for case studies

### 🔍 Dynamic Filtering
- Filter by industry, company size, and success status
- Real-time updates across all visualizations
- Segment-specific analysis capabilities

### 📊 Interactive Visualizations
- Plotly-based charts with hover details and zoom capabilities
- Distribution plots, scatter plots, correlation matrices
- Box plots for comparative analysis
- Bar charts for categorical breakdowns

## Quick Start

### Method 1: Using the Run Script
```bash
./run_app.sh
```

### Method 2: Manual Startup
```bash
# Activate virtual environment
source .venv/bin/activate

# Run Streamlit app
streamlit run streamlit_app.py
```

### Method 3: Background Mode
```bash
cd /home/abdullah/Work/ai-project-dataset-generator
.venv/bin/python -m streamlit run streamlit_app.py --server.headless true --server.port 8501
```

## Access the Dashboard

Once running, open your browser and navigate to:
- **Local URL**: http://localhost:8501
- **Network URL**: http://192.168.0.104:8501 (accessible from other devices on your network)

## Dataset Requirements

The app automatically loads the most recent dataset file:
- Looks for `synthetic_ai_projects_dataset_*.csv` files
- Loads the most recently modified file
- Displays success/error messages

Make sure you have run the `synthetic_ai_dataset_generator.py` script first to generate the dataset.

## Dependencies

All required packages are listed in `requirements.txt`:
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scipy

## Dashboard Sections

### 📊 Overview
- Dataset summary statistics
- Research validation metrics
- MIT J-curve validation
- KPI tracking impact analysis

### 🏢 Company Demographics
- Company size, industry, and regional distributions
- Revenue analysis by company characteristics
- Ownership and growth stage breakdowns

### 🤖 AI Projects
- Project type and complexity analysis
- Investment amount distributions
- AI intensity patterns
- Success rates by project characteristics

### 💰 Business Impact
- Revenue and EBITDA impact distributions
- ROI and payback period analysis
- Industry-specific performance metrics
- Success rate comparisons

### 🔗 Correlations
- MIT J-curve: AI intensity vs revenue growth
- KPI tracking impact on EBITDA
- Company size vs AI maturity correlation
- Comprehensive correlation matrix

### 🎯 Insights
- Key findings and business insights
- Industry performance patterns
- Evidence-based benchmarks (conservative, realistic, stretch goals)
- Recommendations for case studies

## Customization

The dashboard supports various customizations:

### Filters
- **Industry**: Select specific industries or view all
- **Company Size**: Filter by Small, Medium, Large, or all sizes
- **Success Status**: View all projects, successful only, or failed only

### Styling
- Custom CSS for improved visual appeal
- Responsive design for different screen sizes
- Professional color schemes and typography

## Use Cases

### Sales & Marketing
- Evidence-based ROI projections
- Industry-specific benchmarks
- Success story identification
- Competitive positioning

### Consulting & Strategy
- Client presentation materials
- Business case development
- Risk assessment frameworks
- Timeline and investment planning

### Research & Analysis
- Statistical validation of AI investment patterns
- Correlation analysis between variables
- Segment-specific performance analysis
- Benchmarking against research studies

## Technical Notes

### Performance
- Data caching with `@st.cache_data` for fast loading
- Efficient filtering and aggregation
- Optimized visualizations for large datasets

### Error Handling
- Graceful handling of missing data files
- Validation of filter combinations
- Safe mathematical operations (division by zero, etc.)

### Scalability
- Designed to handle datasets with varying sizes
- Efficient memory usage for large datasets
- Responsive UI for different data volumes

## Troubleshooting

### Common Issues

1. **"No dataset file found" error**
   - Run `python synthetic_ai_dataset_generator.py` first
   - Ensure CSV files are in the same directory

2. **Port already in use**
   - Use a different port: `streamlit run streamlit_app.py --server.port 8502`
   - Or kill existing Streamlit processes

3. **Missing dependencies**
   - Install requirements: `pip install -r requirements.txt`
   - Activate virtual environment first

4. **Performance issues**
   - Use filters to reduce dataset size
   - Close unused browser tabs
   - Restart the Streamlit app if needed

## Data Privacy

This dashboard uses synthetic data that:
- ✅ Maintains statistical validity
- ✅ Preserves realistic business correlations
- ✅ Ensures complete confidentiality
- ✅ Provides evidence-based benchmarks

Perfect for client presentations and case studies without any confidentiality concerns!