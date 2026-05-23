FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps for building common wheels
RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential gcc \
	&& rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/
WORKDIR /app/backend

EXPOSE 8000

# Start Uvicorn server (serves app from backend/app.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
