from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
from models import UserCreate, UserLogin
from conexion.dataBase import supabase

router = APIRouter()

@router.post("/register", response_model=UserLogin)
async def register_user(user: UserCreate):
    existing = supabase.table("usuarios").select("email").eq("email", user.email).execute()
    if existing.data: 
        raise HTTPException(status_code=400, detail="Email already in use.")

    hashed_pw = bcrypt.hash(user.password)
    result = supabase.table("usuarios").insert({
        "nombre": user.nombre,
        "email": user.email,
        "password": hashed_pw,
        "rol": "usuario"
    }).execute()

    return {"id_usuario": result.data[0]["id_usuario"], "nombre": user.nombre, "email": user.email, "rol": "usuario"}

@router.post("/login")
async def login_user(user: UserLogin):
    email = user.email
    password = user.password

    # Buscar al usuario en la base de datos
    user_db = supabase.table("usuarios").select("*").eq("email", email).execute()
    if not user_db.data:
        raise HTTPException(status_code=400, detail="Correo electrónico no encontrado.")
    
    stored_pw = user_db.data[0]["password"]
    if not bcrypt.verify(password, stored_pw):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta.")
    
    user_id = user_db.data[0]["id_usuario"]
    role = user_db.data[0]["rol"]

    chats = supabase.table("chat").select("*").eq("usuario_id", user_id).execute()
    if chats.data:
        chat_id = chats.data[0]["id_chat"]
    else:
        new_chat = supabase.table("chat").insert({
            "usuario_id": user_id
        }).execute()

        if not new_chat.data:
            raise HTTPException(status_code=500, detail="Error al crear un nuevo chat.")
        
        chat_id = new_chat.data[0]["id_chat"]

    return {"message": "Login exitoso", "usuario_id": user_id, "role": role, "chat_id": chat_id}
