#!/bin/bash

echo "🚀 Launching Site Capacity Metrics Dashboard..."
echo "=================================="
echo "ℹ️  Note: This script is for LOCAL DEVELOPMENT only"
echo "ℹ️  For Streamlit Cloud deployment, use requirements.txt"
echo ""

# Check if we should use conda or pip
if command -v conda &> /dev/null; then
    echo "🐍 Using Conda environment..."
    # Activate conda environment
    echo "Activating conda environment: capacity_metrics_viz"
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate capacity_metrics_viz
    
    # Check if environment is activated
    if [[ $CONDA_DEFAULT_ENV == "capacity_metrics_viz" ]]; then
        echo "✅ Conda environment activated successfully"
    else
        echo "❌ Failed to activate conda environment"
        echo "💡 Try: conda env create -f environment.yml"
        exit 1
    fi
elif command -v pip &> /dev/null; then
    echo "📦 Using pip environment..."
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "❌ Neither conda nor pip found"
    echo "Please install Python package manager"
    exit 1
fi

echo ""
echo "Starting Streamlit application..."
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

# Run the Streamlit app
streamlit run streamlit_app.py 