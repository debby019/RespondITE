from fastapi import HTTPException
from backend.conexion.dataBase import supabase
from backend.ai.aiEngine import handle_user_input

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
