import os
import requests
from dotenv import load_dotenv
from backend.conexion.dataBase import supabase

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def generate_response(user_input: str, chat_id: str) -> str:
    try:
        response = supabase.table("mensaje").select("*").eq("chat_id", chat_id).order("fecha_envio").execute()
        messages = response.data

        conversation_context = [{"role": "system", "content": "You are a helpful assistant."}]
        role_map = {"usuario": "user", "assistant": "assistant", "system": "system"}

        for message in messages:
            remitente = message.get("remitente", "usuario")
            role = role_map.get(remitente, "user")
            conversation_context.append({"role": role, "content": message["mensaje"]})

        payload = {
            "messages": conversation_context,
            "model": "Meta-Llama-3.1-8B-Instruct"
        }
        print(f"DEBUG Sending to HF Router: {payload}")

        api_response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)

        if api_response.status_code != 200:
            return f"API Error: {api_response.status_code} - {api_response.text}"

        try:
            ai_message = api_response.json()["choices"][0]["message"]["content"]
            supabase.table("mensaje").insert([
                {"chat_id": chat_id, "mensaje": user_input, "remitente": "usuario"},
                {"chat_id": chat_id, "mensaje": ai_message, "remitente": "assistant"}
            ]).execute()
            return ai_message
        except (KeyError, IndexError) as e:
            return f"Error parsing API response: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"

def set_ai_tone(tone: str) -> str:
    if tone == "formal":
        return "You are very polite and formal in your responses."
    elif tone == "casual":
        return "You are friendly and casual in your responses."
    else:
        return "You respond in a neutral tone."

def handle_user_input(user_input: str, chat_id: str, tone: str = "neutral"):
    from backend.textProcessor import get_knowledge_data

    system_message = set_ai_tone(tone)
    supabase.table("mensaje").insert([
        {"chat_id": chat_id, "mensaje": system_message, "remitente": "system"}
    ]).execute()

    knowledge = get_knowledge_data()
    user_question = user_input.lower()

    for key, value in knowledge.items():
        if key.lower() in user_question:
            info_message = f"Información del procedimiento '{key}':\n{value}"
            supabase.table("mensaje").insert([
                {"chat_id": chat_id, "mensaje": info_message, "remitente": "system"}
            ]).execute()
            break

    ai_response = generate_response(user_input, chat_id)
    return ai_response
