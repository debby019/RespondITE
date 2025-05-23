from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.models import *
from backend.logic.user import *
from backend.logic.auth import *

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

@router.post("/auth/guest")
def login_guest():
    guest_user_id = create_guest_user()
    token = crear_token({"sub": guest_user_id, "role": "guest"})
    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "user_id": guest_user_id
    })


@router.post("/delete")
def eliminar_usuario(token_data=Depends(verificar_token)):
    role = token_data.get("role")
    user_id = token_data.get("sub")
    if role == "guest" and user_id:
        delete_user(user_id)
        return {"mensaje": f"Usuario invitado {user_id} eliminado."}
    return {"mensaje":"usuario eliminado"}