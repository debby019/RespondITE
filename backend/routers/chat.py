from fastapi import APIRouter
from models import ChatRequest
from logic.chat import save_user_message, generate_ai_response, get_chat_history_by_chat_id

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    save_user_message(request.chat_id, request.user_input)
    ai_response = generate_ai_response(request.chat_id, request.user_input, request.tone)
    return {"response": ai_response}

@router.get("/chat-history/{chat_id}")
async def get_chat_history(chat_id: str):
    return get_chat_history_by_chat_id(chat_id)
