# backend/main.py

from fastapi import FastAPI, HTTPException
from app.backend.auth import authenticate_user
from app.backend.chat import get_response
from app.schemas.schema import LoginRequest, ChatRequest

app = FastAPI()


@app.post("/login")
def login(data: LoginRequest):
    if authenticate_user(data.username, data.password, data.role):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials or role mismatch")

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        response = get_response(data.query, data.role)
        return {"response": response}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
