from fastapi import APIRouter
from backend.database import conn

router = APIRouter()

@router.get("/history")
def get_history(username: str):
    cur = conn.cursor()
    cur.execute(
        "SELECT query, answer FROM chat_history WHERE username=? ORDER BY id DESC",
        (username,)
    )
    return cur.fetchall()
