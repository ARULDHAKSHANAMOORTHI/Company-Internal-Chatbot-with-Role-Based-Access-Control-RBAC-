
# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from ingest.ingest_docs import load_documents, chunk_documents


# # 1️⃣ Load and chunk documents
# docs = load_documents()
# chunks = chunk_documents(docs)

# print("Loaded docs:", len(docs))
# print("Generated chunks:", len(chunks))

# if not chunks:
#     raise ValueError("❌ No document chunks found. Check data path and file parsing.")


# # 2️⃣ Prepare texts + metadata
# texts = [c["content"] for c in chunks]
# metadatas = [c["metadata"] for c in chunks]


# # 3️⃣ Create embeddings (ONLY ONCE)
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # 4️⃣ Create and persist Chroma DB
# db = Chroma.from_texts(
#     texts=texts,
#     embedding=embeddings,
#     metadatas=metadatas,
#     persist_directory="vector_store/chroma_db"
# )

# db.persist()

# print("✅ Vector DB created successfully")

# import os
# import shutil

# from ingest.ingest_docs import load_documents, chunk_documents
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma


# # ==============================
# # CONFIG
# # ==============================
# VECTOR_DIR = "vector_store/chroma_db"


# # ==============================
# # CLEAN OLD VECTOR DB
# # ==============================
# if os.path.exists(VECTOR_DIR):
#     shutil.rmtree(VECTOR_DIR)
#     print("🗑️ Old vector DB removed")


# # ==============================
# # LOAD + CHUNK DOCUMENTS
# # ==============================
# documents = load_documents()
# chunks = chunk_documents(documents)

# print(f"📄 Loaded documents: {len(documents)}")
# print(f"✂️ Generated chunks: {len(chunks)}")

# if not chunks:
#     raise ValueError("❌ No chunks generated. Check data folder and files.")


# # ==============================
# # EMBEDDINGS
# # ==============================
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )


# # ==============================
# # CREATE VECTOR STORE
# # ==============================
# db = Chroma.from_documents(
#     documents=chunks,
#     embedding=embeddings,
#     persist_directory=VECTOR_DIR
# )

# db.persist()

# print("✅ Vector DB created successfully with role metadata")


import os
import shutil
from ingest.ingest_docs import load_documents, chunk_documents
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DIR = "vector_store/chroma_db"

# 🔥 Clean old vector DB
if os.path.exists(VECTOR_DIR):
    shutil.rmtree(VECTOR_DIR)

print("📄 Loading documents...")
docs = load_documents()

print("✂️ Chunking documents...")
chunks = chunk_documents(docs)

print(f"Docs loaded: {len(docs)}")
print(f"Chunks created: {len(chunks)}")

if not chunks:
    raise RuntimeError("❌ No chunks created. Check data path or parsing.")

# 🔢 Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 📦 Create vector DB
db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory=VECTOR_DIR
)

db.persist()
print("✅ Vector DB created successfully")
