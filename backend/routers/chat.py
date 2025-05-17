from fastapi import APIRouter, Depends, HTTPException
from backend.logic.user import  get_chats_by_user_id
from backend.logic.auth import verificar_token
from backend.models import *
from backend.logic.chat import *
router = APIRouter()

@router.post("/chat")
def chat_endpoint(request: ChatRequest, token_data=Depends(verificar_token)):
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido: falta ID de usuario")

    chat_id = request.chat_id 
    if not chat_id:
        raise HTTPException(status_code=400, detail="Falta el ID del chat")
    save_user_message(chat_id, request.user_input)
    ai_response = generate_ai_response(chat_id, request.user_input, request.tone)
    return {"respuesta": ai_response}



@router.post("/chats/nuevo")
def crear_nuevo_chat(token_data=Depends(verificar_token)):
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    new_id = create_chat(user_id)
    return {"id_chat": new_id}


@router.get("/chats/{chat_id}/mensajes")
async def historial_chat(chat_id: str):
    return get_chat_history_by_chat_id(chat_id)


@router.post("/chats")
def obtener_chats_usuario(request: ChatRequestBody):
    if not request.usuario_id:
        raise HTTPException(status_code=400, detail="Falta el usuario_id")
    
    return get_chats_by_user_id(request.usuario_id)


@router.post("/chats/help")
def solicitar_ayuda(request: HelpRequest):
    help_data = insert_help(request.chat_id)
    return {"mensaje": "Solicitud de ayuda registrada", "data": help_data}