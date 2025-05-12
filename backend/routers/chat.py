from fastapi import APIRouter, Depends, HTTPException
from backend.logic.user import get_or_create_chat
from backend.logic.auth import verificar_token
from backend.models import ChatRequest
from backend.logic.chat import save_user_message, generate_ai_response, get_chat_history_by_chat_id

router = APIRouter()

@router.post("/chat")
def chat_endpoint(request: ChatRequest, token_data=Depends(verificar_token)):
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido: falta ID de usuario")

    chat_id = get_or_create_chat(user_id)
    save_user_message(chat_id, request.user_input)
    ai_response = generate_ai_response(chat_id, request.user_input, request.tone)
    return {"respuesta": ai_response}

@router.get("/chats/{chat_id}/mensajes")
async def historial_chat(chat_id: str):
    return get_chat_history_by_chat_id(chat_id)
