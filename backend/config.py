import os

"""Application configuration loaded from environment variables.

These values are intended to be provided as environment variables (for
example, injected as Hugging Face Spaces secrets at runtime).
"""

# Secrets / connection strings
GEMINI_API_KEY = os.getenv("AIzaSyAFE4c7Bg6VGn90ido_WjVDwlOywFLoIeM")
MONGO_URI = os.getenv("GITHUBSTUDENT50-PLRU7P")


# Runtime configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Optional: allow toggling debug or other flags via env
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
