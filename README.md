# Autonomous AI Data Analyst Platform

---
sdk: docker
app_port: 8000
pinned: false
---

## Overview

This repository contains an Autonomous AI Data Analyst Platform with a Streamlit frontend and FastAPI backend.
The platform is designed to integrate Gemini API for AI insights, MongoDB Atlas for metadata management, Azure Blob Storage for datasets and model artifacts, and Scikit-learn for AutoML.

## Repository Structure

- `frontend/`
  - Streamlit pages and reusable components for the UI.
  - `frontend/Dockerfile` for building the frontend container.
  - `frontend/requirements.txt` for frontend dependencies.

- `backend/`
  - FastAPI application with route handlers and AI agents.
  - Agents for EDA, AutoML, query handling, and insights.
  - Utility modules for database, storage, and AI integration.
  - `backend/Dockerfile` for building the backend container.
  - `backend/requirements.txt` for backend dependencies.

- `.github/workflows/`
  - CI/CD workflows for testing and deploying the platform.

- `.env.example`
  - Example environment variables required to run the platform.

## Environment Variables

Environment variables should be defined in a `.env` file or your deployment environment.

- `GEMINI_API_KEY`
- `MONGO_URI`
- `AZURE_STORAGE_CONN`
- `BACKEND_URL`

## Next Steps

1. Implement Streamlit pages and frontend components.
2. Add FastAPI route logic and agent workflows.
3. Configure CI/CD workflows in GitHub Actions.
4. Connect the backend to MongoDB Atlas and Azure Blob Storage.
5. Integrate Gemini API calls and Scikit-learn AutoML.
