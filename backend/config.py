import os

# Configuration scaffold for environment variables and application settings.
# This file loads GEMINI_API_KEY, MONGO_URI, AZURE_STORAGE_CONN, BACKEND_URL, and other secrets.

GEMINI_API_KEY = os.getenv("AIzaSyAFE4c7Bg6VGn90ido_WjVDwlOywFLoIeM")
MONGO_URI = os.getenv("GITHUBSTUDENT50-PLRU7P")
AZURE_STORAGE_CONN = os.getenv("AZURE_STORAGE_CONN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
