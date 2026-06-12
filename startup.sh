#!/bin/bash
set -e

echo "===== Starting Autonomous AI Data Analyst ====="
echo "🚀 Starting FastAPI backend..."

cd /app/backend

# Start backend and capture output
tmux_pipe="/tmp/backend.log"
uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    2>&1 | tee /tmp/backend.log &

BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo "⏳ Waiting for backend..."
for i in {1..60}; do
    if kill -0 $BACKEND_PID 2>/dev/null; then
        if python -c "import requests; requests.get('http://localhost:8000/health', timeout=2)" 2>/dev/null; then
            echo "✅ Backend is ready!"
            break
        fi
    else
        echo "❌ Backend process died!"
        echo "Backend logs:"
        cat /tmp/backend.log
        exit 1
    fi
    echo "  Attempt $i/60..."
    sleep 1
done

echo "🎨 Starting Streamlit..."
cd /app
exec streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true
