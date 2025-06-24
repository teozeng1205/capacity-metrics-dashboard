# 🚀 Site Capacity Metrics Dashboard

An impressive, interactive Streamlit dashboard for visualizing site capacity metrics with advanced analytics and beautiful visualizations.

## ✨ Features

### 📊 Comprehensive Visualizations
- **Time Series Analysis**: Track performance metrics over time
- **Interactive Heatmaps**: Provider vs hour performance patterns
- **Comparative Analysis**: Provider and site performance comparisons
- **Individual Site Deep Dive**: Detailed analysis for specific sites
- **Data Explorer**: Raw data viewing with sorting and filtering

### 🎛️ Interactive Controls
- **Multi-select Filters**: Choose providers and sites
- **Time Range Selection**: Focus on specific hours
- **Metric Selection**: Switch between TPH, Count Sum, and Response Delay
- **Dynamic Updates**: Real-time chart updates based on filters

### 📈 Key Metrics Displayed
- **TPH (Transactions Per Hour) Median**: Site capacity performance
- **Count Sum**: Total transaction counts
- **Average Response Delay**: System response times in minutes
- **Provider and Site Statistics**: Comprehensive performance overview

## 🛠️ Setup Instructions

### 1. Create Conda Environment

```bash
# Create the environment from the provided environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate capacity_metrics_viz
```

### 2. Alternative Setup (if environment.yml doesn't work)

```bash
# Create environment manually
conda create -n capacity_metrics_viz python=3.10 -y
conda activate capacity_metrics_viz

# Install packages
conda install -c conda-forge streamlit pandas numpy plotly seaborn matplotlib scikit-learn -y
pip install streamlit-plotly-events streamlit-aggrid plotly-express
```

### 3. Run the Dashboard

```bash
# Make sure you're in the project directory
cd capacity_metrics_visualization

# Run the Streamlit app
streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
capacity_metrics_visualization/
├── data/
│   └── site_metrics_final_20250610_to_20250623.csv
├── environment.yml
├── streamlit_app.py
└── README.md
```

## 🎯 How to Use

### 1. **Sidebar Filters**
- Select one or more providers (AI, QL2)
- Choose specific sites or leave all selected
- Adjust hour range (0-23) to focus on specific time periods
- Pick primary metric for main analysis

### 2. **Navigation Tabs**

#### 📈 Time Series
- View hourly trends by provider
- See top 5 sites performance throughout the day
- Identify peak and low performance periods

#### 🗺️ Heatmaps
- Provider vs Hour performance patterns
- Site vs Hour response delay visualization
- Easy identification of performance hotspots

#### 📊 Comparisons
- Provider performance comparison bars
- TPH vs Response Delay scatter plots
- Performance distribution analysis (box/violin plots)

#### 🔍 Site Analysis
- Select individual sites for detailed analysis
- View specific site metrics and trends
- Dual-axis charts for comprehensive insights

#### 📋 Data Table
- Summary statistics for filtered data
- Raw data with sorting capabilities
- Download filtered data as CSV

### 3. **Key Metrics Dashboard**
- Real-time summary statistics
- Quick overview of current filter results
- Performance indicators and ranges

## 🎨 Dashboard Features

### Interactive Elements
- **Hover Information**: Detailed data points on mouseover
- **Cross-filtering**: Charts update based on sidebar selections
- **Responsive Design**: Works on different screen sizes
- **Download Capability**: Export filtered data

### Visual Design
- **Modern UI**: Clean, professional appearance
- **Color Coding**: Intuitive color schemes for different metrics
- **Gradient Headers**: Eye-catching title design
- **Emoji Icons**: Clear visual indicators

## 📊 Data Schema

The dashboard processes the following data columns:
- `providercode`: Provider identifier (AI, QL2)
- `sitecode`: Site identifier 
- `hour`: Hour of day (0-23)
- `tph_median`: Transactions Per Hour median value
- `measure`: Measurement type (TPH)
- `ct_sum`: Count sum of transactions
- `avg_first_resp_delay_minute`: Average first response delay in minutes
- `last_updated`: Timestamp of last data update

## 🚀 Advanced Features

### Performance Insights
- Automatically identifies top-performing sites
- Highlights performance patterns and anomalies
- Provides statistical summaries and distributions

### Data Export
- Download filtered datasets
- Timestamp-based file naming
- CSV format for further analysis

### Responsive Analytics
- Real-time metric calculations
- Dynamic chart updates
- Interactive data exploration

## 🤝 Support

If you encounter any issues:
1. Ensure all dependencies are properly installed
2. Check that the data file exists in the `data/` directory
3. Verify Python and conda versions are compatible
4. Try recreating the conda environment

---

**Built with ❤️ using Streamlit, Plotly, and Python**

*Dashboard created for impressive site capacity metrics visualization* 