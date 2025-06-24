# 🚀 Site Capacity Metrics Dashboard

[![GitHub Stars](https://img.shields.io/github/stars/teozeng1205/capacity-metrics-dashboard?style=social)](https://github.com/teozeng1205/capacity-metrics-dashboard)
[![GitHub Forks](https://img.shields.io/github/forks/teozeng1205/capacity-metrics-dashboard?style=social)](https://github.com/teozeng1205/capacity-metrics-dashboard)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.46+-red.svg)](https://streamlit.io)

An impressive, interactive Streamlit dashboard for visualizing site capacity metrics with advanced analytics and beautiful visualizations.

🔗 **Repository**: [https://github.com/teozeng1205/capacity-metrics-dashboard](https://github.com/teozeng1205/capacity-metrics-dashboard)

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

### 🌐 For Streamlit Cloud Deployment (Recommended)

1. **Fork/Clone this repository** to your GitHub account
2. **Connect to Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io)
3. **Deploy**: Select your repository and `streamlit_app.py` as the main file
4. **Automatic Setup**: Streamlit Cloud will automatically install dependencies from `requirements.txt`

### 🖥️ For Local Development

#### Option 1: Using the Launch Script (Easiest)
```bash
# Make the script executable (first time only)
chmod +x launch_dashboard.sh

# Run the dashboard
./launch_dashboard.sh
```

#### Option 2: Using Conda Environment
```bash
# Create the environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate capacity_metrics_viz

# Run the Streamlit app
streamlit run streamlit_app.py
```

#### Option 3: Using pip
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
capacity_metrics_visualization/
├── data/
│   └── site_metrics_final_20250610_to_20250623.csv  # Dataset
├── streamlit_app.py           # Main dashboard application
├── requirements.txt           # Dependencies for Streamlit Cloud & pip
├── environment.yml           # Dependencies for conda (local development)
├── launch_dashboard.sh       # Local development launch script
├── .gitignore               # Git ignore rules
└── README.md                # This documentation
```

### 📋 Deployment Files
- **For Streamlit Cloud**: Uses `requirements.txt` automatically
- **For Local Development**: Use `environment.yml` (conda) or `requirements.txt` (pip)
- **Launch Script**: `launch_dashboard.sh` for easy local setup

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

## 🔗 Links

- **Repository**: [GitHub](https://github.com/teozeng1205/capacity-metrics-dashboard)
- **Issues**: [Report bugs or request features](https://github.com/teozeng1205/capacity-metrics-dashboard/issues)
- **Discussions**: [Community discussions](https://github.com/teozeng1205/capacity-metrics-dashboard/discussions)

## 🤝 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/teozeng1205/capacity-metrics-dashboard/issues) page
2. Ensure all dependencies are properly installed
3. Check that the data file exists in the `data/` directory
4. Verify Python and conda versions are compatible
5. Try recreating the conda environment

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

**Built with ❤️ using Streamlit, Plotly, and Python**

*Dashboard created for impressive site capacity metrics visualization* 