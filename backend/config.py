import os
from typing import Optional

SUPABASE_URL: Optional[str] = os.environ.get("https://ifaqimxdpcbpfzviygaj.supabase.co")
SUPABASE_ANON_KEY: Optional[str] = os.environ.get("sb_publishable_yJytuCM7_FA7lfvfWOlTFg_epTzkjQD")
GEMINI_API_KEY: Optional[str] = os.environ.get("your-AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")
BACKEND_URL: str = os.environ.get("BACKEND_URL", "http://localhost:8000")
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"

# Validate on startup
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not configured - AI features disabled")
if not SUPABASE_URL:
    print("⚠️  WARNING: SUPABASE_URL not configured - database disabled")
