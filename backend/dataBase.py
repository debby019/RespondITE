import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL and/or SUPABASE_KEY in .env file.")

    return create_client(url, key)

supabase = get_supabase()
