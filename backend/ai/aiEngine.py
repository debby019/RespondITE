import os
import requests
from dotenv import load_dotenv
from supabase import create_client
from backend.conexion.dataBase import supabase

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def generate_response(user_input: str, chat_id: str) -> str:
    try:
        response = supabase.table("mensaje").select("mensaje").eq("chat_id", chat_id).order("fecha_envio").execute()
        if response.error:
            return f"Error fetching conversation history: {response.error.message}"

        messages = response.data
        conversation_context = [{"role": "system", "content": "You are a helpful assistant."}]

        for message in messages:
            conversation_context.append({"role": "usuario", "content": message["mensaje"]})

        payload = {"inputs": conversation_context}
        api_response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)

        if api_response.status_code != 200:
            return f"API Error: {api_response.status_code} - {api_response.text}"

        try:
            ai_message = api_response.json()[0]["generated_text"]
            supabase.table("mensaje").insert([
                {"chat_id": chat_id, "mensaje": user_input, "remitente": "usuario"},
                {"chat_id": chat_id, "mensaje": ai_message, "remitente": "assistant"}
            ]).execute()
            return ai_message
        except (KeyError, IndexError) as e:
            return f"Error parsing API response: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"

# customize AI behavior
def set_ai_tone(tone: str) -> str:
    if tone == "formal":
        return "You are a very polite and formal in your responses."
    elif tone == "casual":
        return "You are friendly and casual in your responses."
    else:
        return "You respond in a neutral tone."

# handle chat messages using the database
def handle_user_input(user_input: str, chat_id: str, tone: str = "neutral"):
    system_message = set_ai_tone(tone)
    supabase.table("mensaje").insert([
        {"chat_id": chat_id, "mensaje": system_message, "remitente": "system"}
    ]).execute()
    ai_response = generate_response(user_input, chat_id)
    return ai_response
