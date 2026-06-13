import os
import sys

# Read from environment with debugging
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Debug output
print(f"[CONFIG] GEMINI_API_KEY set: {bool(GEMINI_API_KEY)}", file=sys.stderr)
print(f"[CONFIG] SUPABASE_URL set: {bool(SUPABASE_URL)}", file=sys.stderr)

if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not configured", file=sys.stderr)
