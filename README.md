---
title: Autonomous AI Data Analyst
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.28.0"
python_version: "3.12"
app_file: app.py
pinned: false
---

# 📊 Autonomous AI Data Analyst

Production-ready AI-powered data analysis platform with a Perplexity-like chat interface.

## Features

✅ Clean, minimal Perplexity-like UI with animations
✅ CSV upload and instant preview
✅ Natural language to pandas code conversion
✅ AI-powered data insights
✅ Professional logging system
✅ Comprehensive test suite (95%+ coverage)
✅ GitHub Actions CI/CD
✅ Type hints on all functions
✅ Docker deployment ready
✅ Works on HuggingFace Spaces

## Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python async)
- **AI**: Google Gemini API
- **Testing**: pytest with coverage
- **Deployment**: Docker + HuggingFace Spaces

## Quick Start

### Local Development

```bash
git clone https://github.com/Virajdouelectron/Autonomous-AI-Data-Analyst-Platform
cd Autonomous-AI-Data-Analyst-Platform

cp .env.example .env
# Edit .env with your API keys

make install
make test
make run
```

### Deploy to HuggingFace Spaces

1. Create new Space (Docker SDK)
2. Set Secrets in Space Settings:
   - GEMINI_API_KEY
   - BACKEND_URL=http://localhost:8000
3. Push code:
   ```bash
   git push hf main
   ```

## Project Structure

```
Autonomous-AI-Data-Analyst-Platform/
├── .github/workflows/tests.yml
├── Dockerfile
├── startup.sh
├── Makefile
├── requirements.txt
├── app.py (Streamlit frontend)
├── .env.example
├── .gitignore
├── README.md
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── logging_config.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── upload.py
│   │   ├── query.py
│   │   ├── insights.py
│   │   └── modeling.py
│   └── tests/
│       ├── conftest.py
│       ├── test_upload.py
│       ├── test_health.py
│       ├── test_query.py
│       └── test_insights.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/upload` | POST | Upload CSV |
| `/api/query` | POST | Generate pandas code |
| `/api/insights` | POST | Generate AI insights |
| `/api/train-model` | POST | Train ML model |

## Testing

```bash
make test
```

Coverage report available in `htmlcov/index.html`

## Commands

```bash
make install    # Install dependencies
make test       # Run tests with coverage
make run        # Run locally
make lint       # Lint code
make format     # Format with black
make clean      # Clean cache
```

## Environment Variables

- `GEMINI_API_KEY` - Google Gemini API key (required for AI features)
- `BACKEND_URL` - Backend API URL (default: http://localhost:8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `DEBUG` - Debug mode (default: False)
