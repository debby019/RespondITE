from fastapi import HTTPException
from passlib.hash import bcrypt
from conexion.dataBase import supabase
from models import UserCreate

def get_user_by_email(email: str):
    result = supabase.table("usuarios").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None

def create_user(user: UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    result = supabase.table("usuarios").insert({
        "nombre": user.nombre,
        "email": user.email,
        "password": hashed_pw,
        "rol": "usuario"
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Error al registrar el usuario.")
    
    return result.data[0]

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

def get_or_create_chat(user_id: int):
    chats = supabase.table("chat").select("*").eq("usuario_id", user_id).execute()
    if chats.data:
        return chats.data[0]["id_chat"]
    
    new_chat = supabase.table("chat").insert({"usuario_id": user_id}).execute()
    if not new_chat.data:
        raise HTTPException(status_code=500, detail="Error al crear un nuevo chat.")
    
    return new_chat.data[0]["id_chat"]
