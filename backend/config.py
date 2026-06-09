import os

def get_supabase_url():
	return os.environ.get("https://ifaqimxdpcbpfzviygaj.supabase.co")


def get_supabase_key():
	return os.environ.get("sb_publishable_yJytuCM7_FA7lfvfWOlTFg_epTzkjQD")


def get_gemini_key():
	return os.environ.get("AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")


BACKEND_URL = os.environ.get("http://localhost:8000")

# Still expose as module-level for backwards compatibility
SUPABASE_URL = os.environ.get("https://ifaqimxdpcbpfzviygaj.supabase.co")
SUPABASE_ANON_KEY = os.environ.get("sb_publishable_yJytuCM7_FA7lfvfWOlTFg_epTzkjQD")
GEMINI_API_KEY = os.environ.get("AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")
