import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory if it exists
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"[CONFIG] Loaded .env from {env_path}", file=sys.stderr)

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
    print("[CONFIG] WARNING: GEMINI_API_KEY not configured", file=sys.stderr)
