import os

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not set")
if not SUPABASE_URL:
    print("Warning: SUPABASE_URL not set")
