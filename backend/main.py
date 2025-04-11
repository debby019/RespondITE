from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from aiEngine import handle_user_input
from passlib.hash import bcrypt
from dataBase import supabase

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register_user(nombre: str = Form(...), email: str = Form(...), password: str = Form(...)):
    existing = supabase.table("Usuarios").select("Email").eq("Email", email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already in use.")

    hashed_pw = bcrypt.hash(password)
    result = supabase.table("Usuarios").insert({
        "Nombre": nombre,
        "Email": email,
        "Password": hashed_pw,
        "Rol": "usuario"
    }).execute()
    return {"message": "User registered successfully."}

@app.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    user = supabase.table("Usuarios").select("*").eq("Email", email).execute()
    if not user.data:
        raise HTTPException(status_code=400, detail="Invalid entry.")

    stored_pw = user.data[0]["Password"]
    if not bcrypt.verify(password, stored_pw):
        raise HTTPException(status_code=400, detail="Invalid entry.")

    user_id = user.data[0]["ID_usuario"]
    role = user.data[0]["Rol"]

    # check if chats already exist
    chats = supabase.table("Chat").select("*").eq("Usuario_id", user_id).execute()
    if chats.data:
        chat_id = chats.data[0]["ID_Chat"]
    else:
        new_chat = supabase.table("Chat").insert({
            "Usuario_id": user_id
        }).execute()
        chat_id = new_chat.data[0]["ID_Chat"]

    return {
        "message": "Login successful",
        "usuario_id": user_id,
        "role": role,
        "chat_id": chat_id
    }

# Request model
class ChatRequest(BaseModel):
    user_input: str
    tone: str = "neutral"
    chat_id: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_msg = supabase.table("Mensaje").insert({
        "Chat_id": request.chat_id,
        "Mensaje": request.user_input,
        "Remitente": "usuario"
    }).execute()

    ai_response = handle_user_input(request.user_input, chat_id=request.chat_id, tone=request.tone)
    ai_msg = supabase.table("Mensaje").insert({
        "Chat_id": request.chat_id,
        "Mensaje": ai_response,
        "Remitente": "ia"
    }).execute()
    return {"response": ai_response}

@app.get("/chat-history/{chat_id}")
async def get_chat_history(chat_id: str):
    try:
        result = supabase.table("Mensaje").select("*").eq("Chat_id", chat_id).order("Fecha_Envio", desc=False).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server (if running as a script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
