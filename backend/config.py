import os

"""Application configuration loaded from environment variables.

These values are intended to be provided as environment variables (for
example, injected as Hugging Face Spaces secrets at runtime).
"""

# Secrets / connection strings (read from environment / secrets manager)
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if not MONGO_URI:
	print("⚠️ WARNING: MONGO_URI not set. Database features will be disabled.")
	MONGO_URI = None


# Runtime configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Optional: allow toggling debug or other flags via env
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
