# from fastapi import FastAPI
# from backend.auth import router as auth_router
# from backend.rag import rag_response
# from backend.middleware import get_user

# app = FastAPI(title="Infosys Internal Chatbot")

# app.include_router(auth_router)

# @app.post("/chat")
# def chat(query: str, request):
#     user = get_user(request)
#     return rag_response(query, user["role"], user["sub"])

# @app.get("/")
# def root():
#     return {"status": "Backend running"}

# from fastapi import FastAPI
# from backend.auth import router as auth_router
# from backend.rag import router as rag_router
# from backend.history import router as history_router

# app = FastAPI()

# app.include_router(auth_router)
# app.include_router(rag_router)
# app.include_router(history_router)

# @app.get("/")
# def root():
#     return {"status": "Backend running"}


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import conn
from backend.auth import hash_password, verify_password, create_token

app = FastAPI()

# -------- SCHEMAS --------
class SignupRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

# -------- SIGNUP --------
@app.post("/signup")
def signup(data: SignupRequest):
    cur = conn.cursor()

    if data.role not in ["c_level", "finance", "marketing", "hr", "engineering", "employees"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (data.username, hash_password(data.password), data.role)
        )
        conn.commit()
        return {"message": "User created successfully"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

# -------- LOGIN --------
@app.post("/login")
def login(data: LoginRequest):
    cur = conn.cursor()
    cur.execute(
        "SELECT password, role FROM users WHERE username=?",
        (data.username,)
    )
    row = cur.fetchone()

    if not row or not verify_password(data.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(data.username, row[1])
    return {"token": token}
