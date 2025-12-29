# vector_store/index_data.py

from preprocessing.ingest import run_preprocessing
from vector_store.embedder import EmbeddingModel
from vector_store.chroma_db import get_chroma_client, get_collection

def index_documents():
    chunks = run_preprocessing()
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]

    embedder = EmbeddingModel()
    embeddings = embedder.embed(texts)

    client = get_chroma_client()
    collection = get_collection(client)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    print(f"Indexed {len(texts)} chunks into ChromaDB")

if __name__ == "__main__":
    index_documents()
