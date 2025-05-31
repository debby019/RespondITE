
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Modelo para registrar un nuevo usuario
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

# Modelo de respuesta al registrar un usuario (sin contraseña)
class RegisterResponse(BaseModel):
    id_usuario: str
    nombre: str
    email: str
    rol: str

# Modelo para iniciar sesión
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Cuerpo de una solicitud de chat del usuario
class ChatRequest(BaseModel):
    user_input: str
    chat_id: Optional[str]
    tone: Optional[str] = "neutral"

# Modelo para representar un mensaje
class Message(BaseModel):
    chat_id: str
    mensaje: str
    remitente: str

# Modelo para crear un nuevo chat
class ChatRequestBody(BaseModel):
    usuario_id: str

class HelpRequest(BaseModel):
    chat_id: str


class Consulta(BaseModel):
    consulta: str
    informacion: str


class ProcesoBase(BaseModel):
    nombre: str
    consultas: List[Consulta]

class ProcesoCreate(ProcesoBase):
    ...

class ProcesoUpdate(ProcesoBase):
    ...


class ProcesoOut(ProcesoBase):
    id_proceso: str

    class Config:
        from_attributes = True
