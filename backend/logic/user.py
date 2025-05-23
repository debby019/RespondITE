from fastapi import HTTPException
from passlib.hash import bcrypt
from backend.conexion.dataBase import supabase
from backend.models import UserCreate
import uuid


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

def create_guest_user():
    guest_id = str(uuid.uuid4())
    result = supabase.table("usuarios").insert({
        "id_usuario": guest_id,
        "nombre": f"invitado_{guest_id[:8]}",
        "email": f"{guest_id}@guest.local",    # Email falso
        "password": "",                        # campo requerido, aunque no lo usaremos
        "rol": "guest",
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="No se pudo crear el usuario invitado.")
    
    return guest_id


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

def get_chats_by_user_id(user_id: str):
    result = supabase.table("chat").select("*").eq("usuario_id", user_id).order("fecha_inicio", desc=True).execute()
    for chat in result.data:
        print(chat["id_chat"], chat["fecha_inicio"])

    if not result.data:
        print("no funciono")
        return []
    return result.data

def delete_user(user_id: str):

    supabase.table("usuarios").delete().eq("id_usuario", user_id).execute()
    