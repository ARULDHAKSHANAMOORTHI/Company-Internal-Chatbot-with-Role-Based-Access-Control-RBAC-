
# # import os
# # from dotenv import load_dotenv
# # from google import genai
# # from backend.search import search_docs

# # # Load environment variables
# # load_dotenv()

# # API_KEY = os.getenv("GEMINI_API_KEY")
# # if not API_KEY:
# #     raise RuntimeError("GEMINI_API_KEY not set")

# # # Initialize Gemini client
# # client = genai.Client(api_key=API_KEY)

# # MODEL_NAME = "models/gemini-flash-lite-latest"

# # def rag_response(query: str, role: str):
# #     """
# #     RAG response using vector search + Gemini
# #     """
# #     docs = search_docs(query, role)

# #     if docs:
# #         context = "\n\n".join(d["content"] for d in docs)
# #         sources = list(set(d["source"] for d in docs))
# #     else:
# #         context = "No relevant internal documents found."
# #         sources = []

# #     prompt = f"""
# # You are an internal company chatbot.
# # Answer professionally and clearly using ONLY the context below.

# # Context:
# # {context}

# # User Question:
# # {query}
# # """

# #     response = client.models.generate_content(
# #         model=MODEL_NAME,
# #         contents=prompt
# #     )

# #     return {
# #         "answer": response.text,
# #         "sources": sources
# #     }


# # import os
# # from dotenv import load_dotenv
# # from google import genai

# # from backend.search import search_docs
# # from backend.audit import log_access


# # # ==============================
# # # ENV + GEMINI SETUP
# # # ==============================
# # load_dotenv()

# # API_KEY = os.getenv("GEMINI_API_KEY")
# # if not API_KEY:
# #     raise RuntimeError("❌ GEMINI_API_KEY not set")

# # client = genai.Client(api_key=API_KEY)

# # MODEL_NAME = "models/gemini-flash-lite-latest"


# # # ==============================
# # # RAG RESPONSE
# # # ==============================
# # def rag_response(query: str, role: str, user="terminal"):
# #     """
# #     RAG pipeline:
# #     1. Role-based vector search
# #     2. Context-grounded LLM response
# #     3. Audit logging
# #     """

# #     # 🔍 Vector search with RBAC
# #     docs = search_docs(query, role)

# #     # ❌ No documents found
# #     if not docs:
# #         return {
# #             "answer": "No relevant internal documents found.",
# #             "sources": [],
# #             "confidence": 0.0
# #         }

# #     # 📊 Confidence (simple heuristic)
# #     confidence = round(min(len(docs) / 5, 1.0), 2)

# #     # 📚 Build context from Document objects
# #     context = "\n\n".join(doc.page_content for doc in docs)

# #     # 🧠 Prompt (STRICT grounding)
# #     prompt = f"""
# # You are an internal company chatbot.

# # Answer ONLY using the information in the context.
# # If the answer is not present, say "No relevant internal documents found."

# # Context:
# # {context}

# # Question:
# # {query}
# # """

# #     # 🤖 Gemini response
# #     response = client.models.generate_content(
# #         model=MODEL_NAME,
# #         contents=prompt
# #     )

# #     answer = response.text.strip()

# #     # 🧾 Audit log
# #     log_access(user, role, query, docs)

# #     return {
# #         "answer": answer,
# #         "sources": list(set(doc.metadata.get("source", "unknown") for doc in docs)),
# #         "confidence": confidence
# #     }


# # from backend.search import search_docs
# # from backend.llm import generate_answer
# # from backend.audit import log_access

# # def rag_response(query: str, role: str, user="terminal"):
# #     docs = search_docs(query, role)

# #     if not docs:
# #         return {
# #             "answer": "No relevant internal documents found.",
# #             "sources": [],
# #             "confidence": 0.0
# #         }

# #     context = "\n\n".join(d.page_content for d in docs)

# #     prompt = f"""
# # You are an internal company chatbot.
# # Answer ONLY using the context below.

# # Context:
# # {context}

# # Question:
# # {query}
# # """

# #     answer = generate_answer(prompt)

# #     log_access(user, role, query, docs)

# #     confidence = round(min(len(docs) / 5, 1.0), 2)

# #     return {
# #         "answer": answer,
# #         "sources": list(set(d.metadata.get("source") for d in docs)),
# #         "confidence": confidence
# #     }


# from backend.search import search_docs
# from backend.query_utils import normalize_query
# from backend.llm import generate_answer

# def rag_response(query: str, role: str, username: str):
#     query = normalize_query(query)

#     # 👋 Greeting handling
#     if query in ["hi", "hello", "hey"]:
#         return {
#             "answer": "Hello! How can I assist you with internal company information?",
#             "sources": [],
#             "confidence": 1.0
#         }

#     docs = search_docs(query, role)
#     print(f"Retrieved docs: {len(docs)}")

#     if not docs:
#         return {
#             "answer": "No relevant internal documents found.",
#             "sources": [],
#             "confidence": 0.0
#         }

#     context = "\n\n".join(d.page_content for d in docs)
#     sources = list(set(d.metadata["source"] for d in docs))

#     confidence = round(min(len(docs) / 5, 1.0), 2)

#     prompt = f"""
# You are an internal company chatbot.
# Answer ONLY using the context below.

# Context:
# {context}

# Question:
# {query}
# """

#     answer = generate_answer(prompt)

#     return {
#         "answer": answer,
#         "sources": sources,
#         "confidence": confidence
#     }
# @router.post("/chat")
# def chat(query: str, token: str):
#     payload = jwt.decode(token, SECRET, algorithms=["HS256"])
#     username = payload["sub"]
#     role = payload["role"]

#     result = rag_response(query, role, username)
#     return result

# from backend.database import conn

# cur = conn.cursor()
# cur.execute(
#     "INSERT INTO chat_history (username, query, answer) VALUES (?, ?, ?)",
#     (username, query, answer)
# )
# conn.commit()


from fastapi import APIRouter
import jwt

from backend.search import search_docs
from backend.query_utils import normalize_query
from backend.llm import generate_answer
from backend.database import conn

SECRET = "secret123"  # same secret used in auth
router = APIRouter()


# ===============================
# RAG CORE FUNCTION
# ===============================
def rag_response(query: str, role: str, username: str):
    query = normalize_query(query)

    # 👋 Greeting handling
    if query in ["hi", "hello", "hey"]:
        return {
            "answer": "Hello! How can I assist you with internal company information?",
            "sources": [],
            "confidence": 1.0
        }

    # 🔍 Role-based retrieval
    docs = search_docs(query, role)
    print(f"Retrieved docs: {len(docs)}")

    if not docs:
        answer = "No relevant internal documents found."
        confidence = 0.0
        sources = []
    else:
        context = "\n\n".join(d.page_content for d in docs)
        sources = list(set(d.metadata.get("source", "unknown") for d in docs))
        confidence = round(min(len(docs) / 5, 1.0), 2)

        prompt = f"""
You are an internal company chatbot.
Answer ONLY using the context below.

Context:
{context}

Question:
{query}
"""
        answer = generate_answer(prompt)

    # 🧾 Store chat history
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history (username, query, answer) VALUES (?, ?, ?)",
        (username, query, answer)
    )
    conn.commit()

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }


# ===============================
# FASTAPI CHAT ENDPOINT
# ===============================
@router.post("/chat")
def chat(query: str, token: str):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    username = payload["sub"]
    role = payload["role"]

    return rag_response(query, role, username)
