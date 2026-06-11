#!/bin/bash
set -e

echo "===== Starting Autonomous AI Data Analyst ====="
echo "🚀 Starting FastAPI backend..."

cd /app/backend
uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info &
BACKEND_PID=$!

echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if python -c "import requests; requests.get('http://localhost:8000/health')" 2>/dev/null; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

echo "🎨 Starting Streamlit frontend..."
cd /app
streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --logger.level=info
