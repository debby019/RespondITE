from fastapi import APIRouter
from backend.models import ChatRequest
from backend.logic.chat import save_user_message, generate_ai_response, get_chat_history_by_chat_id

router = APIRouter()

# meter aqui el @router.post("/chat")

# Enviar mensaje y obtener respuesta de IA
@router.post("/chats/{chat_id}/mensajes")
async def enviar_mensaje(chat_id: str, request: ChatRequest):
    save_user_message(chat_id, request.user_input)
    ai_response = generate_ai_response(chat_id, request.user_input, request.tone)
    return {"response": ai_response}

# Obtener historial del chat
@router.get("/chats/{chat_id}/mensajes")
async def historial_chat(chat_id: str):
    return get_chat_history_by_chat_id(chat_id)
