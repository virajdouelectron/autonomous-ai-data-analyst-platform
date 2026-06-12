import os

SUPABASE_URL = os.environ.get("sb_url_https://your-supabase-url.supabase.co")
SUPABASE_ANON_KEY = os.environ.get("sb_publishable_yJytuCM7_FA7lfvfWOlTFg_epTzkjQD")
GEMINI_API_KEY = os.environ.get("your-AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")
BACKEND_URL = os.environ.get("http://localhost:8000")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Just print warnings, don't crash
if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY not set")
if not SUPABASE_URL:
    print("⚠️ SUPABASE_URL not set")
