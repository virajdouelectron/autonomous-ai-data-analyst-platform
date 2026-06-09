import os

"""Application configuration loaded from environment variables.

These values are intended to be provided as environment variables (for
example, injected as Hugging Face Spaces secrets at runtime).
"""

# Secrets / connection strings (read from environment / secrets manager)
SUPABASE_URL = os.getenv("https://ifaqimxdpcbpfzviygaj.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_yJytuCM7_FA7lfvfWOlTFg_epTzkjQD")
GEMINI_API_KEY = os.getenv("AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")

if not SUPABASE_URL or not SUPABASE_KEY:
	print("⚠️ WARNING: SUPABASE_URL or SUPABASE_ANON_KEY not set. Database features will be disabled.")


# Runtime configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Optional: allow toggling debug or other flags via env
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
