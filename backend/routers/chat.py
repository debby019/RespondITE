from fastapi import APIRouter, HTTPException
from models import ChatRequest
from ai.aiEngine import handle_user_input
from conexion.dataBase import supabase

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    user_msg = supabase.table("mensaje").insert({
        "chat_id": request.chat_id,
        "mensaje": request.user_input,
        "remitente": "usuario"
    }).execute()

    ai_response = handle_user_input(request.user_input, chat_id=request.chat_id, tone=request.tone)
    ai_msg = supabase.table("mensaje").insert({
        "chat_id": request.chat_id,
        "mensaje": ai_response,
        "remitente": "assistant"
    }).execute()
    return {"response": ai_response}

@router.get("/chat-history/{chat_id}")
async def get_chat_history(chat_id: str):
    try:
        result = supabase.table("mensaje").select("*").eq("chat_id", chat_id).order("fecha_envio", desc=False).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
