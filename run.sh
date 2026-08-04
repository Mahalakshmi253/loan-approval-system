#!/bin/bash

# Loan Approval System Startup Script

set -e

echo "🏦 Loan Approval System - Startup"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
fi

# Start backend in background
echo ""
echo "🚀 Starting FastAPI backend on http://127.0.0.1:8000..."
python -m backend.main &
BACKEND_PID=$!
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Failed to start backend"
    exit 1
fi
echo "✓ Backend started (PID: $BACKEND_PID)"

# Start Streamlit
echo ""
echo "🎨 Starting Streamlit UI on http://127.0.0.1:8501..."
streamlit run frontend/streamlit_app.py

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT

echo ""
echo "✓ All services stopped"
