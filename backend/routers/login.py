from fastapi import APIRouter, HTTPException
from backend.models import UserCreate, UserLogin, RegisterResponse
from backend.logic.user import get_user_by_email, create_user, verify_password
from backend.logic.auth import crear_token

router = APIRouter()

@router.post("/register", response_model= RegisterResponse)
async def register_user(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Correo ya registrado.")

    created_user = create_user(user)
    return {
        "id_usuario": created_user["id_usuario"],
        "nombre": user.nombre,
        "email": user.email,
        "rol": "usuario"
    }

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Correo electrónico no encontrado.")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta.")
    
    token_data = {
        "sub": str(db_user["id_usuario"]),
        "role": db_user["rol"]
    }
    token = crear_token(token_data)
    return {
        "message": "Login exitoso",
        "token": token,
        "usuario_id": db_user["id_usuario"],
        "role": db_user["rol"],
    }
