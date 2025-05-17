from fastapi import HTTPException
from backend.conexion.dataBase import supabase
from backend.ai.aiEngine import handle_user_input
from backend.models import *

def save_user_message(chat_id: str, mensaje: str):
    result = supabase.table("mensaje").insert({
        "chat_id": chat_id,
        "mensaje": mensaje,
        "remitente": "usuario"
    }).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al guardar el mensaje del usuario.")

def generate_ai_response(chat_id: str, user_input: str, tone: str):
    response = handle_user_input(user_input, chat_id=chat_id, tone=tone)
    result = supabase.table("mensaje").insert({
        "chat_id": chat_id,
        "mensaje": response,
        "remitente": "assistant"
    }).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Error al guardar el mensaje de la IA.")
    return response

def get_chat_history_by_chat_id(chat_id: str):
    try:
        result = supabase.table("mensaje").select("*").eq("chat_id", chat_id).order("fecha_envio", desc=False).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def create_chat(user_id: str):
    new_chat = supabase.table("chat").insert({"usuario_id": user_id}).execute()
    if not new_chat.data:
        raise HTTPException(status_code=500, detail="Error al crear un nuevo chat.")
    return new_chat.data[0]["id_chat"]

def insert_help(chat_id: str):
    new_help = supabase.table("help_request").insert({"chat_id": chat_id,
                                                      "estado": "pendiente"}).execute()
    if not new_help.data:
        raise HTTPException(status_code=500, detail="Error al guardar la solicitud de ayuda.")
    return new_help.data[0]
