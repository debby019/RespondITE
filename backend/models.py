from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    id_usuario: str
    nombre: str
    email: str
    rol: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    user_input: str
    chat_id: Optional[str]
    tone: Optional[str] = "neutral"


class Message(BaseModel):
    chat_id: str
    mensaje: str
    remitente: str

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
