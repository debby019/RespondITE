from fastapi import HTTPException
from passlib.hash import bcrypt
from backend.conexion.dataBase import supabase
from backend.models import UserCreate
import uuid

# Obteniene un usuario por correo electrónico
def get_user_by_email(email: str):
    result = supabase.table("usuarios").select("*").eq("email", email).execute()
    return result.data[0] if result.data else None

# Crea un usuario nuevo, hasheando su contraseña con bcrypt
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

# Crear un usuario invitado (temporal)
def create_guest_user():
    guest_id = str(uuid.uuid4())
    result = supabase.table("usuarios").insert({
        "id_usuario": guest_id,
        "nombre": f"invitado_{guest_id[:8]}",   #Nombre temporal
        "email": f"{guest_id}@guest.local",    # Email temporal
        "password": "",                        
        "rol": "guest",
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="No se pudo crear el usuario invitado.")
    
    return guest_id

#Verifica si la contraseña corresponde con el hash almacenado
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.verify(plain_password, hashed_password)

# Obtiene todos los chats asociados a un usuario.
def get_chats_by_user_id(user_id: str):
    result = supabase.table("chat").select("*").eq("usuario_id", user_id).order("fecha_inicio", desc=True).execute()
    for chat in result.data:
        print(chat["id_chat"], chat["fecha_inicio"])

    if not result.data:
        print("no funciono")
        return []
    return result.data

# Elimina un usuario por su ID
def delete_user(user_id: str):
    supabase.table("usuarios").delete().eq("id_usuario", user_id).execute()
    