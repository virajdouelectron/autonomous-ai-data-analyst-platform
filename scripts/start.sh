#!/bin/bash
# Startup script for running both FastAPI backend and Streamlit frontend in the same container
# ISSUE 2 FIX: This script enables deployment on HuggingFace Spaces with both services running

set -e

echo "Starting Autonomous AI Data Analyst Platform..."
echo ""

# Start FastAPI backend on port 8000 in the background
echo "🚀 Starting FastAPI backend on port 8000..."
cd /app/backend
uvicorn app:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Give FastAPI time to start
sleep 2

# Start Streamlit frontend on port 7860
echo "🚀 Starting Streamlit frontend on port 7860..."
cd /app
streamlit run app.py --server.port 7860 --server.address 0.0.0.0

# Cleanup on exit
trap "kill $FASTAPI_PID 2>/dev/null || true" EXIT
