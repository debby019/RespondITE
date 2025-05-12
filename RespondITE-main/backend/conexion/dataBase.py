# Conexión a la BD
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")

    return create_client(url, key)


supabase = get_supabase()
