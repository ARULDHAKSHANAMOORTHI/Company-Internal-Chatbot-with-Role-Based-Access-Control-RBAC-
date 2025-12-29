from loader import load_markdown_files
from cleaner import clean_text
from chunker import chunk_text
from metadata import assign_metadata

def run_preprocessing():
    all_documents = load_markdown_files()
    all_chunks = []

    for doc in all_documents:
        cleaned_text = clean_text(doc["content"])
        chunks = chunk_text(cleaned_text)
        metadata_chunks = assign_metadata(
            chunks,
            doc["source"],
            doc["department"]
        )
        all_chunks.extend(metadata_chunks)

    return all_chunks

if __name__ == "__main__":
    processed_data = run_preprocessing()
    print(f"Total chunks created: {len(processed_data)}")

    # sample output
    print(processed_data[0])
