# Multi-service Dockerfile for HuggingFace Spaces
# Runs both FastAPI backend and Streamlit frontend in a single container
# HuggingFace Spaces required: port 7860 exposed for Streamlit

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
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
