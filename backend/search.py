

# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# # IMPORTANT: Must be SAME model used during ingestion
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # Load persisted Chroma DB
# vectordb = Chroma(
#     persist_directory="vector_store/chroma_db",
#     embedding_function=embeddings
# # )

# # def search_docs(query: str, role: str, k: int = 8):
# #     """
# #     Searches vector DB and returns relevant documents
# #     """
# #     docs = vectordb.similarity_search(query, k=k)

# #     print("Retrieved docs:", len(docs))  # DEBUG (remove later)

# #     results = []
# #     for doc in docs:
# #         results.append({
# #             "content": doc.page_content,
# #             "source": doc.metadata.get("source", "unknown")
# #         })

# #     return results


# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# db = Chroma(
#     persist_directory="vector_store/chroma_db",
#     embedding_function=embeddings
# )

# # def search_docs(query: str, role: str, k: int = 5):
# #     results = db.similarity_search(query, k=k)

# #     allowed_docs = []
# #     for doc in results:
# #         roles = doc.metadata.get("roles", "")
# #         if role in roles.split(","):
# #             allowed_docs.append(doc)

# #     print(f"Retrieved docs: {len(allowed_docs)}")
# #     return allowed_docs

# def search_docs(query, role):
#     results = db.similarity_search(query, k=5)

#     allowed = []
#     for doc in results:
#         roles = doc.metadata.get("roles", "")
#         role_list = [r.strip().lower() for r in roles.split(",")]

#         if role.lower() in role_list or "c_level" in role_list:
#             allowed.append(doc)

#     return allowed


# backend/search.py

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from backend.rbac import allowed_roles

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="vector_store/chroma_db",
    embedding_function=embeddings
)

def search_docs(query: str, role: str, k: int = 5):
    allowed = allowed_roles(role)
    results = db.similarity_search(query, k=10)

    filtered = []
    for doc in results:
        roles = doc.metadata.get("roles", "").split(",")
        if any(r in allowed for r in roles):
            filtered.append(doc)

    return filtered[:k]
