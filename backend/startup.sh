#!/bin/bash
set -e

echo "===== Starting Autonomous AI Data Analyst ====="
echo "🚀 Starting FastAPI backend..."

cd /app/backend

# Start backend with explicit error handling
uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info 2>&1 | tee backend.log &
BACKEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "⏳ Waiting for backend to be ready..."

# Wait up to 60 seconds for backend
for i in {1..60}; do
    echo "Attempt $i/60..."
    if python -c "import requests; r = requests.get('http://localhost:8000/health', timeout=2); print('Backend OK'); r.raise_for_status()" 2>/dev/null; then
        echo "✅ Backend is ready!"
        break
    fi
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process died. Showing logs:"
        cat backend.log
        exit 1
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
