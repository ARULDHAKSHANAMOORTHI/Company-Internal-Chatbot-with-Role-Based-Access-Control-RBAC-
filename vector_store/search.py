from vector_store.chroma_db import get_chroma_client, get_collection
from vector_store.embedder import EmbeddingModel
from vector_store.rbac import can_access
from vector_store.query_utils import normalize_query

def semantic_search(query, user_role, top_k=5):
    query = normalize_query(query)

    embedder = EmbeddingModel()
    query_embedding = embedder.embed([query])[0]

    client = get_chroma_client()
    collection = get_collection(client)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    filtered_results = []

    for doc, meta, score in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if can_access(user_role, meta["roles"]):
            filtered_results.append({
                "content": doc,
                "metadata": meta,
                "score": score
            })

    return filtered_results
