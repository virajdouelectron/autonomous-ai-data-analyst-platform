FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt backend/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r backend/requirements.txt

COPY . .

RUN chmod +x startup.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

EXPOSE 7860

CMD ["./startup.sh"]
