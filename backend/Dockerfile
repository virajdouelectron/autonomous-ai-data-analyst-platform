FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps for building common wheels
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential gcc \
	&& rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./requirements.txt
COPY backend/requirements.txt ./backend_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
	pip install --no-cache-dir -r backend_requirements.txt

# Copy backend and frontend source
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY app.py ./app.py
COPY scripts/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 7860

# ISSUE 2 FIX: Use startup script to run both FastAPI and Streamlit in the same container
# This enables deployment on HuggingFace Spaces where both services need to run together
CMD ["/app/start.sh"]
