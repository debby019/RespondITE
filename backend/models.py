from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    user_input: str
    tone: str = "neutral"
    chat_id: str


class Message(BaseModel):
    chat_id: str
    mensaje: str
    remitente: str
