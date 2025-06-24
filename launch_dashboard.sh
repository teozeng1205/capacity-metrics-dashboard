#!/bin/bash

echo "🚀 Launching Site Capacity Metrics Dashboard..."
echo "=================================="

# Activate conda environment
echo "Activating conda environment: capacity_metrics_viz"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate capacity_metrics_viz

# Check if environment is activated
if [[ $CONDA_DEFAULT_ENV == "capacity_metrics_viz" ]]; then
    echo "✅ Environment activated successfully"
else
    echo "❌ Failed to activate environment"
    exit 1
fi

echo "Starting Streamlit application..."
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

# Run the Streamlit app
streamlit run streamlit_app.py 