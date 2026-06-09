# 📋 COMPLETE CODE REFERENCE - ALL CHANGES

## NEW FILES CREATED

### 1. ROOT LEVEL: `Dockerfile`
```dockerfile
# Multi-service Dockerfile for HuggingFace Spaces
# Runs both FastAPI backend and Streamlit frontend in a single container
# HuggingFace Spaces required: port 7860 exposed for Streamlit

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY backend/requirements.txt ./backend-requirements.txt
COPY requirements.txt ./frontend-requirements.txt

# Install dependencies from both frontend and backend
RUN pip install --no-cache-dir -r backend-requirements.txt && \
    pip install --no-cache-dir -r frontend-requirements.txt

# Copy entire project structure
COPY . .

# Make startup script executable
RUN chmod +x /app/startup.sh

# Expose both ports:
# - 8000 for FastAPI backend
# - 7860 for Streamlit frontend (HuggingFace Spaces requirement)
EXPOSE 8000 7860

# Health check for HuggingFace Spaces
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

# Run the startup script which orchestrates both services
CMD ["/app/startup.sh"]
```

---

### 2. ROOT LEVEL: `startup.sh`
```bash
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
cd /app/backend
uvicorn app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info &

FASTAPI_PID=$!
echo "   FastAPI PID: $FASTAPI_PID"

# Give FastAPI time to start
sleep 3

# Check if FastAPI started successfully
if ! kill -0 $FASTAPI_PID 2>/dev/null; then
    echo "❌ FastAPI failed to start"
    exit 1
fi

echo "✓ FastAPI started successfully"
echo ""

# Start Streamlit frontend on port 7860 in the foreground (main process)
echo "🎨 Starting Streamlit frontend on port 7860..."
cd /app
streamlit run app.py \
    --server.port=7860 \
    --server.address=0.0.0.0 \
    --logger.level=info \
    --client.toolbarMode=viewer

# Cleanup on exit
trap "kill $FASTAPI_PID 2>/dev/null || true" EXIT
```

---

### 3. ROOT LEVEL: `.env.example`
```bash
# Environment Configuration Example
# Copy this file to .env and fill in your actual values for local development
# For HuggingFace Spaces, set these in the Space Settings > Secrets

# Supabase project URL and anon key for data persistence
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key

# Google Gemini API Key for AI-powered insights
GEMINI_API_KEY=your_gemini_api_key_here

# Backend URL (used by Streamlit frontend to call backend API)
# For local development: http://localhost:8000
# For HuggingFace Spaces: http://localhost:8000 (same container deployment)
BACKEND_URL=http://localhost:8000

# Optional: Debug mode
DEBUG=false
```

---

### 4. NEW: `backend/utils/json_utils.py`
```python
"""Utility functions for JSON serialization and data cleaning."""
import numpy as np
import pandas as pd
from typing import Any, Dict, List


def clean_dataframe_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NaN and inf values in DataFrame with None for JSON serialization.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with NaN and inf values replaced with None
    """
    df = df.copy()
    # Replace inf and -inf with None
    df = df.replace([np.inf, -np.inf], None)
    # Replace NaN with None
    df = df.where(pd.notnull(df), None)
    return df


def _clean_list_nan(lst: List[Any]) -> List[Any]:
    """Recursively replace NaN and inf values in a list with None."""
    cleaned_lst = []
    for v in lst:
        if isinstance(v, float):
            if np.isnan(v) or np.isinf(v):
                cleaned_lst.append(None)
            else:
                cleaned_lst.append(v)
        elif isinstance(v, dict):
            cleaned_lst.append(clean_dict_nan(v))
        elif isinstance(v, list):
            cleaned_lst.append(_clean_list_nan(v))
        else:
            cleaned_lst.append(v)
    return cleaned_lst


def clean_dict_nan(data: Dict[str, Any]) -> Dict[str, Any]:
    """Replace NaN and inf values in dict with None for JSON serialization.
    
    Args:
        data: Input dictionary
        
    Returns:
        Dictionary with NaN and inf values replaced with None
    """
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, float):
            if np.isnan(value) or np.isinf(value):
                cleaned[key] = None
            else:
                cleaned[key] = value
        elif isinstance(value, dict):
            cleaned[key] = clean_dict_nan(value)
        elif isinstance(value, list):
            cleaned[key] = _clean_list_nan(value)
        else:
            cleaned[key] = value
    return cleaned


def convert_dataframe_to_json_serializable(df: pd.DataFrame, orient: str = "records") -> Any:
    """Convert DataFrame to JSON-serializable format.
    
    Args:
        df: Input DataFrame
        orient: Orientation for to_dict() method
        
    Returns:
        JSON-serializable data (dict or list of dicts)
    """
    df_clean = clean_dataframe_nan(df)
    return df_clean.to_dict(orient=orient)
```

---

## MODIFIED FILES

### 5. `backend/app.py` - UPDATED
**Changes:**
- Added import: `from utils.json_utils import clean_dataframe_nan`
- Updated `/upload` endpoint to use `clean_dataframe_nan()`

**Key Section:**
```python
@app.post("/upload")
async def upload_data(payload: List[Dict]):
    """Receive uploaded CSV data as JSON list of records.
    
    NaN and inf values are automatically cleaned to ensure JSON serialization succeeds.
    """
    df = pd.DataFrame(payload)
    df_clean = clean_dataframe_nan(df)
    cleaned_records = df_clean.to_dict(orient="records")
    
    return {
        "received": len(cleaned_records),
        "status": "success",
        "message": "CSV data uploaded and cleaned successfully"
    }
```

---

### 6. `backend/routes/insight.py` - UPDATED
**Changes:**
- Added imports: `from utils.json_utils import clean_dataframe_nan, clean_dict_nan`
- Updated `insights_from_dataset()` to clean DataFrame output before JSON conversion

**Key Section:**
```python
@router.post("/insights/from_dataset", response_model=DatasetInsightResponse)
def insights_from_dataset(request: DatasetInsightRequest):
    """Fetch dataset by id, compute stats & correlations, call Gemini, save insight, return it."""
    from utils.db import get_dataset, save_insight
    from utils.stats import compute_missing_value_analysis
    from utils.ai import generate_insight_from_stats

    df = get_dataset(request.dataset_id)

    # Clean NaN/inf values before JSON serialization
    df_describe = df.describe(include="all") if not df.empty else pd.DataFrame()
    df_corr = df.corr(numeric_only=True) if not df.empty else pd.DataFrame()
    
    describe_json = json.loads(clean_dataframe_nan(df_describe).to_json()) if not df_describe.empty else {}
    corr_json = json.loads(clean_dataframe_nan(df_corr).to_json()) if not df_corr.empty else {}
    missing = compute_missing_value_analysis(df)
    
    stats = {
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "describe": describe_json,
        "corr": corr_json,
        "missing": missing,
    }
    
    insights_text = generate_insight_from_stats(stats, system_prompt=request.system_prompt)
    insight_id = save_insight(request.dataset_id, insights_text, metadata=...)
    
    return DatasetInsightResponse(insight_id=insight_id, insights=insights_text)
```

---

### 7. `backend/routes/query.py` - UPDATED
**Changes:**
- Added imports: `from utils.json_utils import clean_dataframe_nan, clean_dict_nan`
- Updated `make_result_json_serializable()` to use json_utils functions

**Key Section:**
```python
def make_result_json_serializable(result: any) -> dict | None:
    """Convert query results to JSON-serializable format, replacing NaN/inf with None."""
    if result is None:
        return None
    
    if isinstance(result, pd.DataFrame):
        df_clean = clean_dataframe_nan(result)
        return df_clean.to_dict(orient="records")
    
    if isinstance(result, pd.Series):
        df = result.to_frame()
        df_clean = clean_dataframe_nan(df)
        return df_clean.to_dict(orient="records")
    
    if isinstance(result, dict):
        return clean_dict_nan(result)
    
    return None
```

---

### 8. `backend/routes/ml.py` - UPDATED
**Changes:**
- Added import: `from utils.json_utils import clean_dict_nan`
- Updated `train_model()` to clean metrics and feature importance dicts

**Key Section:**
```python
@router.post("/train", response_model=TrainResponse)
def train_model(request: TrainRequest):
    """Train AutoML models on a dataset retrieved from MongoDB."""
    result = train_dataset_model(
        dataset_id=request.dataset_id,
        target_column=request.target_column,
        test_size=request.test_size,
        random_state=request.random_state,
    )
    
    # Clean NaN/inf values using utility function
    result["best_model_metrics"] = clean_dict_nan(result["best_model_metrics"])
    
    if result.get("best_model_feature_importance"):
        result["best_model_feature_importance"] = clean_dict_nan(result["best_model_feature_importance"])
    
    # Clean all candidate model metrics
    for model_name, model_data in result.get("candidate_models", {}).items():
        if isinstance(model_data, dict) and "metrics" in model_data:
            model_data["metrics"] = clean_dict_nan(model_data["metrics"])
        if isinstance(model_data, dict) and "feature_importance" in model_data and model_data["feature_importance"]:
            model_data["feature_importance"] = clean_dict_nan(model_data["feature_importance"])
    
    return TrainResponse(**result)
```

---

### 9. `README.md` - UPDATED
**Sections Added:**
- 🚀 Quick Start (Local Development & Docker)
- 🌐 Deploy to HuggingFace Spaces (with step-by-step guide)
- 📋 API Endpoints reference
- 🏗️ Project Structure overview
- 🔧 Environment Variables documentation
- 🛠️ Tech Stack details
- 📊 Key Features list
- 📝 Troubleshooting section
- 📚 Resources and references

---

## FILES ALREADY CORRECT (No changes needed)

✅ **backend/config.py**
- Already reads `BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")`
- Already reads `GEMINI_API_KEY`, `SUPABASE_URL`, and `SUPABASE_ANON_KEY` from environment
- No changes required

✅ **root app.py**
- Already reads `BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")`
- All API calls use the environment variable
- No changes required

✅ **frontend/pages/home.py**
- Already has `clean_dataframe_for_json()` function
- Already cleans NaN/inf before upload
- No changes required

✅ **backend/utils/stats.py**
- Already handles NaN/inf in statistics calculations
- No changes required

---

## QUICK START COMMANDS

### For Local Development:
```bash
# Terminal 1: Backend
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
export $(cat .env | xargs)
streamlit run app.py
```

### For Docker Local:
```bash
docker build -t ai-analyst:latest .
docker run -it --env-file .env -p 7860:7860 -p 8000:8000 ai-analyst:latest
```

### For HuggingFace Spaces:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/autonomous-ai-data-analyst
git push hf main
```

---

## SUMMARY OF CHANGES

| Task | Status | Files Changed |
|------|--------|---------------|
| Create root Dockerfile | ✅ | `Dockerfile` (NEW) |
| Create startup script | ✅ | `startup.sh` (NEW) |
| Fix backend URLs | ✅ | Already correct in `backend/config.py` |
| Fix frontend URLs | ✅ | Already correct in `root app.py` |
| Fix NaN serialization | ✅ | `backend/utils/json_utils.py` (NEW), `backend/app.py`, `backend/routes/*.py` |
| Create .env template | ✅ | `.env.example` (NEW) |
| Update README | ✅ | `README.md` (UPDATED) |

---

✅ **ALL TASKS COMPLETED AND READY FOR DEPLOYMENT!**
