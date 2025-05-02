from pydantic import BaseModel, EmailStr

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
    tone: str = "neutral"


class Message(BaseModel):
    chat_id: str
    mensaje: str
    remitente: str
