#!/bin/bash

# FRED - Quick Start Script

echo "🎙️  Starting FRED - File Response & Emotion-based Delivery"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p outputs

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Launching Streamlit app..."
echo ""

# Run the app
streamlit run app.py
