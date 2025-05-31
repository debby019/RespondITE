from dotenv import load_dotenv
import os

# Carga las variables definidas en el archivo .env
load_dotenv()

# obtiene una variable de entorno como número entero.
def extract_number(key, default):
    try:
        return int(os.getenv(key, "").strip())
    except (ValueError, TypeError, AttributeError):
        return default

# obtiene una variable de entorno como cadena.
def extract_string(key, default=""):
    value = os.getenv(key)
    return value.strip() if value else default

SECRET_KEY = extract_string("SECRET_KEY") # Clave secreta para firmar tokens
ALGORITHM = extract_string("ALGORITHM", "HS256")  # Algoritmo para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = extract_number("ACCESS_TOKEN_EXPIRE_MINUTES", 60) # Expiración del token

SUPABASE_URL = extract_string("SUPABASE_URL")
SUPABASE_KEY = extract_string("SUPABASE_KEY")
API_URL = extract_string("API_URL")
API_KEY = extract_string("API_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY no definida en .env")


