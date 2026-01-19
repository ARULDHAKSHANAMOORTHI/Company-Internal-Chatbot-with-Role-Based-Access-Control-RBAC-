from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="vector_store/chroma_db",
    embedding_function=embeddings
)

docs = db.similarity_search("purpose", k=10)

print(f"Found {len(docs)} docs\n")

for d in docs:
    print("CONTENT:", d.page_content[:300])
    print("ROLES:", d.metadata.get("roles"))
    print("SOURCE:", d.metadata.get("source"))
    print("-" * 40)
