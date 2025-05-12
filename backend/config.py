from dotenv import load_dotenv
import os

load_dotenv()

def extract_number(key, default):
    try:
        return int(os.getenv(key, "").strip())
    except (ValueError, TypeError, AttributeError):
        return default

def extract_string(key, default=""):
    value = os.getenv(key)
    return value.strip() if value else default

SECRET_KEY = extract_string("SECRET_KEY")
ALGORITHM = extract_string("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = extract_number("ACCESS_TOKEN_EXPIRE_MINUTES", 60)

SUPABASE_URL = extract_string("SUPABASE_URL")
SUPABASE_KEY = extract_string("SUPABASE_KEY")
API_URL = extract_string("API_URL")
API_KEY = extract_string("API_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no definida en .env")

print(f"DEBUG: ACCESS_TOKEN_EXPIRE_MINUTES = {ACCESS_TOKEN_EXPIRE_MINUTES}")
