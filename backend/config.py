import os

# Read from environment, fresh each time
SUPABASE_URL = os.environ.get("https://ifaqimxdpcbpfzviygaj.supabase.co")
SUPABASE_ANON_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYXFpbXhkcGNicGZ6dml5Z2FqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEwMjM2NjEsImV4cCI6MjA5NjU5OTY2MX0.8T_p32c4P3y09WWjga6eNjHWB52CMNHUzoQ_7odGM1Q")
GEMINI_API_KEY = os.environ.get("AIzaSyB5gT_CxP_Un3t1Cfh36pnYRM6oOvgtOac")
BACKEND_URL = os.environ.get( "http://localhost:8000")

# Debug logging (remove after testing)
if not SUPABASE_URL:
    print("⚠️ SUPABASE_URL not set - database disabled")
if not SUPABASE_ANON_KEY:
    print("⚠️ SUPABASE_ANON_KEY not set - database disabled")
