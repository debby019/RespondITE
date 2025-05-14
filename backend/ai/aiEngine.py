import os
import requests
from dotenv import load_dotenv
from backend.conexion.dataBase import supabase

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def set_ai_tone(tone: str) -> str:
    if tone == "formal":
        return "Eres un asistente académico muy formal y respetuoso."
    elif tone == "casual":
        return "Eres un asistente académico amigable y relajado"
    else:
        return "Responde en un tono académico neutral."

def get_chat_context(chat_id: str, limit: int = 5):
    # Read the last N messages
    result = supabase.table("mensaje").select("*").eq("chat_id", chat_id).order("fecha_envio", desc=True).limit(limit).execute()
    messages = result.data or []
    # Get them in chronological order
    return list(reversed(messages))

def generate_response(user_input: str, knowledge_data: dict, chat_history: list) -> str:
    try:
        catalogue = "\n".join(
            [f"- {k}: {v}" for k, v in knowledge_data.items()]
        )
        history = "\n".join(
            [f"{m['remitente']}: {m['mensaje']}" for m in chat_history if m['remitente'] in ['usuario', 'assistant']]
        )

        system_prompt = (
            "Eres un asistente académico para Servicios Escolares.\n"
            "Solo puedes responder usando la información oficial proporcionada.\n"
            "Si no encuentras ninguna coincidencia, responde exactamente: 'Lo siento, no encontré información relacionada con tu solicitud.'\n\n"
            f"Estas son las categorías oficiales disponibles:\n{catalogue}\n\n"
            f"Esta ha sido la conversación hasta ahora:\n{history}\n\n"
            f"El usuario ahora pregunta: {user_input}\n\n"
            "Selecciona la categoría más adecuada y respnde usando solo esa información.\n"
            "No inventes ni añadas datos externos."
        )

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "model": "Meta-Llama-3.1-8B-Instruct"
        }
        print(f"DEBUG Sending to HF Router: {payload}")
        api_response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)

        if api_response.status_code != 200:
            return f"API Error: {api_response.status_code} - {api_response.text}"

        try:
            ai_message = api_response.json()["choices"][0]["message"]["content"]
            return ai_message
        except (KeyError, IndexError) as e:
            return f"Error al analizar respuesta de la API: {str(e)}"

    except Exception as e:
        return f"Error inesperado: {str(e)}"

def handle_user_input(user_input: str, chat_id: str, tone: str = "neutral"):
    from backend.textProcessor import get_knowledge_data

    system_message = set_ai_tone(tone)
    supabase.table("mensaje").insert([
        {"chat_id": chat_id, "mensaje": system_message, "remitente": "system"}
    ]).execute()

    chat_history = get_chat_context(chat_id)
    knowledge = get_knowledge_data()

    ai_response = generate_response(user_input, knowledge, chat_history)

    supabase.table("mensaje").insert([
        {"chat_id": chat_id, "mensaje": user_input, "remitente": "usuario"},
        {"chat_id": chat_id, "mensaje": ai_response, "remitente": "assistant"}
    ]).execute()

    return ai_response
