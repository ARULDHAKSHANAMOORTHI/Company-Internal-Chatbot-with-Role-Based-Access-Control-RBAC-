from config import ROLE_ACCESS

def assign_metadata(chunks, source, department):
    metadata_chunks = []

    allowed_roles = ROLE_ACCESS.get(department, ["Employees"])

    for i, chunk in enumerate(chunks):
        metadata_chunks.append({
            "chunk_id": f"{source}_chunk_{i}",
            "text": chunk,
            "metadata": {
                "source": source,
                "department": department,
                "roles": allowed_roles
            }
        })

    return metadata_chunks
