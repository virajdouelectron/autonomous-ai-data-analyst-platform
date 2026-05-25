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

# Register trap immediately so it's active during startup checks and Streamlit run
trap "kill $FASTAPI_PID 2>/dev/null || true" EXIT

# Verify process is running
if ! kill -0 $FASTAPI_PID 2>/dev/null; then
    echo "❌ FastAPI process is not running."
    exit 1
fi

# Poll HTTP health endpoint
echo "⏳ Waiting for FastAPI backend to become ready..."
TIMEOUT=30
ELAPSED=0
SUCCESS=false

while [ $ELAPSED -lt $TIMEOUT ]; do
    if python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=1)" >/dev/null 2>&1; then
        SUCCESS=true
        break
    fi
    if ! kill -0 $FASTAPI_PID 2>/dev/null; then
        echo "❌ FastAPI process died."
        break
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
done

if [ "$SUCCESS" = false ]; then
    echo "❌ FastAPI health check failed. Terminating..."
    exit 1
fi

echo "✓ FastAPI is up and healthy!"
echo ""

# Start Streamlit frontend on port 7860
echo "🚀 Starting Streamlit frontend on port 7860..."
cd /app
streamlit run app.py --server.port 7860 --server.address 0.0.0.0
