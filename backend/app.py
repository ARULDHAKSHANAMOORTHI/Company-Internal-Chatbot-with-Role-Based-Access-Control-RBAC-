
from fastapi import FastAPI, HTTPException
from backend.auth import login
from backend.rag import rag_response
import jwt, os

app = FastAPI(title="Infosys Internal Chatbot")

SECRET = os.getenv("JWT_SECRET")

def get_user(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login")
def user_login(username: str, password: str):
    return {"token": login(username, password)}


@app.post("/chat")
def chat(query: str, token: str):
    user = get_user(token)
    return rag_response(query, user["role"])


@app.get("/")
def root():
    return {"status": "Chatbot backend running"}
