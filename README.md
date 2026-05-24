---
---
title: Autonomous AI Data Analyst
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---
---

# ⚙️ AI Data Analyst Backend

This repository contains the FastAPI backend for the Autonomous AI Data Analyst Platform. The API handles CSV storage and retrieval, automated EDA, AI-driven insights via the Gemini API, natural-language-to-Pandas query translation, and simple AutoML model training using Scikit-learn.

## What the API does
- Accepts and stores uploaded CSV datasets for later processing and retrieval.
- Runs automated Exploratory Data Analysis (EDA) and returns summary statistics and visualizations.
- Generates AI-driven insights and business summaries using the Gemini API.
- Translates natural-language queries into Pandas operations and returns query results.
- Trains AutoML models (classification/regression) with Scikit-learn and returns evaluation metrics and trained model artifacts.

## API Endpoints

| Endpoint | Method | Description |
|---|---:|---|
| `/upload` | POST | Upload a CSV file; stores file and returns a dataset ID and metadata. |
| `/insights` | POST | Request automated EDA and AI insights for a dataset ID; returns summaries, charts, and AI-generated findings. |
| `/query` | POST | Send a natural-language question and dataset ID; returns translated Pandas result or a structured answer. |
| `/train` | POST | Start AutoML training on a dataset ID and target column; returns training status, metrics, and model info. |

## Tech stack
- **API framework:** FastAPI
- **AI / LLM:** Gemini API
- **Database / Storage:** MongoDB Atlas
- **ML library:** Scikit-learn
- **Deployment:** Docker

## Environment variables
- `MONGO_URI`: MongoDB connection string used to connect to MongoDB Atlas. The backend uses this to store dataset metadata, file references, model artifacts, and results.
- `GEMINI_API_KEY`: API key (or credential) for accessing the Gemini API. The backend uses this key to request AI-generated insights and to translate NL queries.

Place the variables in your environment or in container secrets before starting the service.

---
Backend README for Hugging Face Space (docker SDK) configuration and API reference.