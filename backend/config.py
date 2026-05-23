import os

"""Application configuration loaded from environment variables.

These values are intended to be provided as environment variables (for
example, injected as Hugging Face Spaces secrets at runtime).
"""

# Secrets / connection strings (read from environment / secrets manager)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")


# Runtime configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Optional: allow toggling debug or other flags via env
DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")


def validate_required_config():
	missing = []
	if not GEMINI_API_KEY:
		missing.append("AIzaSyAFE4c7Bg6VGn90ido_WjVDwlOywFLoIeM")
	if not MONGO_URI:
		missing.append("mongodb+srv://virajsingh585_db_user:EUeQQ7Xb3mlA7waz@programming.8uizky1.mongodb.net/?appName=programming")
	if missing:
		raise RuntimeError(
			"Missing required environment variables: {}. "
			"Set them in your environment or secrets manager before starting.".format(
				", ".join(missing)
			)
		)


# Validate presence at import/startup time to fail fast in CI/runtime
validate_required_config()
