#!/bin/bash
# Startup script to run both FastAPI and Streamlit services in the same container
# This enables full-stack deployment on HuggingFace Spaces

set -e

echo "=========================================="
echo "🚀 Starting Autonomous AI Data Analyst Platform"
echo "=========================================="
echo ""

# Export environment variables if .env exists (for local testing)
if [ -f "/app/.env" ]; then
    echo "📝 Loading environment variables from .env"
    set -a
    source /app/.env
    set +a
fi

# Validate required environment variables
echo "✓ Checking configuration..."
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "⚠️  WARNING: SUPABASE_URL or SUPABASE_ANON_KEY not set. Database operations will fail."
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY not set. AI features will fail."
fi

# Set BACKEND_URL if not provided (default to localhost for same-container deployment)
if [ -z "$BACKEND_URL" ]; then
    export BACKEND_URL="http://localhost:8000"
    echo "✓ BACKEND_URL set to default: $BACKEND_URL"
else
    echo "✓ BACKEND_URL: $BACKEND_URL"
fi

echo ""
echo "=========================================="
echo "🔧 Starting Services"
echo "=========================================="
echo ""

# Start FastAPI backend on port 8000 in the background
echo "📡 Starting FastAPI backend on port 8000..."
cd /app/backend && uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info &

FASTAPI_PID=$!
echo "   FastAPI PID: $FASTAPI_PID"

# Register trap immediately so it is active during health checks and streamlit run
trap "kill $FASTAPI_PID 2>/dev/null || true" EXIT

# Ensure curl is available
if ! command -v curl &> /dev/null; then
    echo "❌ curl is not installed. Exiting..."
    exit 1
fi

# Verify process is running
if ! kill -0 $FASTAPI_PID 2>/dev/null; then
    echo "❌ FastAPI process is not running."
    exit 1
fi

# Poll HTTP health endpoint using curl
echo "⏳ Waiting for FastAPI backend to become ready..."
TIMEOUT=30
ELAPSED=0
SUCCESS=false

while [ $ELAPSED -lt $TIMEOUT ]; do
    if curl -s -f http://localhost:8000/health >/dev/null 2>&1; then
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

echo "✓ FastAPI started successfully and is accepting HTTP connections"
echo ""

# Start Streamlit frontend on port 7860 in the foreground (main process)
echo "🎨 Starting Streamlit frontend on port 7860..."
cd /app
streamlit run app.py \
    --server.port=7860 \
    --server.address=0.0.0.0 \
    --logger.level=info \
    --client.toolbarMode=viewer
