from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class ChatRequest(BaseModel):
    query: str
    role: str
    