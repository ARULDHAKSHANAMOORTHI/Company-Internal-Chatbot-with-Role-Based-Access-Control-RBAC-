# # # backend/auth.py

# # import jwt
# # import datetime
# # import os
# # from dotenv import load_dotenv
# # from fastapi import HTTPException

# # from backend.database import conn

# # # Load environment variables
# # load_dotenv()

# # SECRET = os.getenv("JWT_SECRET")
# # if not SECRET:
# #     raise RuntimeError("❌ JWT_SECRET not set in .env file")


# # def login(username: str, password: str):
# #     cur = conn.cursor()
# #     cur.execute(
# #         "SELECT role FROM users WHERE username=? AND password=?",
# #         (username, password)
# #     )
# #     user = cur.fetchone()

# #     if not user:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")

# #     payload = {
# #         "sub": username,
# #         "role": user[0],
# #         "iat": datetime.datetime.utcnow(),
# #         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
# #     }

# #     token = jwt.encode(payload, SECRET, algorithm="HS256")
# #     return token


# import jwt, datetime, os
# from fastapi import APIRouter, HTTPException
# from backend.database import conn

# router = APIRouter()
# SECRET = os.getenv("JWT_SECRET")

# @router.post("/login")
# def login(username: str, password: str):
#     cur = conn.cursor()
#     cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
#     user = cur.fetchone()

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     payload = {
#         "sub": username,
#         "role": user[0],
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
#     }

#     token = jwt.encode(payload, SECRET, algorithm="HS256")
#     return {"token": token}

import jwt, datetime, os
from fastapi import APIRouter, HTTPException
from backend.database import conn


router = APIRouter()
SECRET = os.getenv("JWT_SECRET", "secret123")

@router.post("/signup")
def signup(username: str, password: str, role: str):
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, password, role.lower())
        )
        conn.commit()
        return {"status": "User created"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login(username: str, password: str):
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": username,
        "role": row[0],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return {"token": token}
