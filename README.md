---
---
title: Autonomous AI Data Analyst
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---
---

# 📊 Autonomous AI Data Analyst Platform

A full-stack AI data analysis platform featuring a Streamlit frontend and FastAPI backend. Upload CSV files, generate business insights using Google's Gemini API, run natural language queries with AutoML model training—all in one sleek interface.

**🎯 Now with single-container deployment for HuggingFace Spaces!**

---

## 🚀 Quick Start

### Local Development

#### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo>
cd Autonomous-AI-Data-Analyst-Platform

# Create Python virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# MONGO_URI=your_mongo_connection_string
# GEMINI_API_KEY=your_gemini_key
```

#### 2. Install Dependencies
```bash
# Install all dependencies (frontend + backend)
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

#### 3. Run Locally (Two Terminal Windows)

**Terminal 1 - Start FastAPI Backend:**
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
# From root directory, with .env variables loaded
export $(cat .env | xargs)
streamlit run app.py
```

The app will open at `http://localhost:8501` and connect to backend at `http://localhost:8000`.

---

### Docker (Local or HuggingFace Spaces)

#### 1. Build Docker Image
```bash
docker build -t ai-analyst:latest .
```

#### 2. Run Locally
```bash
docker run -it \
  -e MONGO_URI="your_mongo_uri" \
  -e GEMINI_API_KEY="your_gemini_key" \
  -e BACKEND_URL="http://localhost:8000" \
  -p 7860:7860 \
  -p 8000:8000 \
  ai-analyst:latest
```

Access the app at `http://localhost:7860`

---

## 🌐 Deploy to HuggingFace Spaces (FREE!)

### Step 1: Create HuggingFace Space
1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click **Create New Space**
3. Choose:
   - **Space name**: `autonomous-ai-data-analyst`
   - **License**: `openrail`
   - **SDK**: `Docker`
   - **Visibility**: `Public` (or `Private`)

### Step 2: Set Environment Secrets
In your Space Settings > Secrets, add:

```
MONGO_URI = mongodb+srv://username:password@cluster.mongodb.net/db_name
GEMINI_API_KEY = your_gemini_api_key_here
BACKEND_URL = http://localhost:8000
```

⚠️ **Important**: Keep `BACKEND_URL=http://localhost:8000` since both services run in the same container.

### Step 3: Push Code to Space
```bash
# Add HuggingFace remote to your git repo
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/autonomous-ai-data-analyst

# Push the code (this will trigger Docker build & deployment)
git push hf main
```

Or manually upload the files through HuggingFace web interface.

### Step 4: Monitor Deployment
HuggingFace will:
1. Build the Docker image using the root `Dockerfile`
2. Run the `startup.sh` script
3. Start FastAPI on port 8000 (background)
4. Start Streamlit on port 7860 (main process)
5. Expose your Space at `https://huggingface.co/spaces/YOUR_USERNAME/autonomous-ai-data-analyst`

---

## 📋 What This App Does

### Backend API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check for monitoring |
| `/upload` | POST | Upload CSV dataset; returns dataset ID |
| `/api/insights` | POST | Generate AI insights from data statistics |
| `/api/insights/from_dataset` | POST | Generate insights from stored dataset |
| `/api/query` | POST | Translate natural language to Pandas code |
| `/api/query/dataset` | POST | Execute query on stored dataset |
| `/api/train` | POST | Train AutoML models on dataset |

### Frontend Pages
- **Home**: Upload CSV, preview data, generate insights
- **Insights**: Request business summaries using Gemini
- **Query**: Natural language to Pandas translation
- **Modeling**: AutoML model training with metrics

---

## 🏗️ Project Structure

```
Autonomous-AI-Data-Analyst-Platform/
├── Dockerfile                 # Root Dockerfile for Docker SDK deployment
├── startup.sh                 # Startup script (FastAPI + Streamlit)
├── .env.example              # Environment template
├── app.py                    # Streamlit entry point (port 7860)
├── requirements.txt          # Frontend dependencies
│
├── backend/
│   ├── app.py               # FastAPI main app (port 8000)
│   ├── config.py            # Environment configuration
│   ├── requirements.txt      # Backend dependencies
│   ├── agents/              # AI agent implementations
│   ├── routes/              # API route handlers
│   └── utils/               # Database, stats, AI helpers
│
├── frontend/
│   ├── pages/               # Streamlit page modules
│   │   ├── home.py
│   │   ├── insights.py
│   │   ├── query.py
│   │   └── modeling.py
│   └── components/          # Reusable UI components
│
└── README.md                # This file
```

---

## 🔧 Environment Variables

### Required (HuggingFace Spaces Secrets)
- `MONGO_URI` - MongoDB Atlas connection string
- `GEMINI_API_KEY` - Google Gemini API key

### Optional
- `BACKEND_URL` - Backend API URL (default: `http://localhost:8000`)
- `DEBUG` - Debug mode toggle (default: `false`)

For local development, create a `.env` file:
```bash
cp .env.example .env
# Then edit .env with your credentials
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: FastAPI (async Python API)
- **Database**: MongoDB Atlas (cloud document DB)
- **AI/LLM**: Google Gemini API (insights & query translation)
- **ML**: Scikit-learn (AutoML model training)
- **Deployment**: Docker + HuggingFace Spaces

---

## 📊 Key Features

✅ **CSV Upload & Preview** - Drag-and-drop file upload with automatic visualization
✅ **Exploratory Data Analysis** - Missing values, statistics, data types
✅ **AI-Powered Insights** - Business summaries using Gemini API
✅ **Natural Language Queries** - Ask questions in plain English, get Pandas code
✅ **AutoML Training** - Automatic model selection, hyperparameter tuning
✅ **Metadata Persistence** - Store datasets, insights, and models in MongoDB
✅ **Responsive UI** - Mobile-friendly Streamlit interface
✅ **Production Ready** - Environment-based config, health checks, error handling

---

## 🚀 How Deployment Works on HuggingFace Spaces

1. **Single Docker Container**: Both frontend (Streamlit) and backend (FastAPI) run in the same container
2. **Startup Process** (`startup.sh`):
   - Starts FastAPI on `0.0.0.0:8000` in background
   - Starts Streamlit on `0.0.0.0:7860` as main process (HF Spaces requirement)
3. **Inter-service Communication**: Streamlit frontend calls backend at `http://localhost:8000`
4. **Port 7860**: Only Streamlit (port 7860) is exposed to the internet by HuggingFace
5. **Health Checks**: Docker includes health check for monitoring

---

## 📝 Troubleshooting

### "Connection refused" error in Streamlit
- **Cause**: FastAPI backend hasn't started yet
- **Fix**: Wait 5-10 seconds for backend to start, then refresh browser

### "Max retries exceeded" error
- **Cause**: Backend URL is incorrect
- **Fix**: Check `BACKEND_URL` env var is set correctly (should be `http://localhost:8000` for HF Spaces)

### "Missing required environment variables" error
- **Cause**: `MONGO_URI` or `GEMINI_API_KEY` not set
- **Fix**: Add them to HuggingFace Space Secrets or local `.env` file

### Docker build fails
- **Cause**: Missing Python dependencies
- **Fix**: Ensure both `requirements.txt` files exist and are valid
- **Check**: `pip install -r requirements.txt && pip install -r backend/requirements.txt`

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [HuggingFace Spaces](https://huggingface.co/spaces)
- [Docker Documentation](https://docs.docker.com/)

---

## 📄 License

This project is open source. Check `LICENSE` file for details.

---

**🎉 Ready to deploy? Push to HuggingFace Spaces and share your Space link!**