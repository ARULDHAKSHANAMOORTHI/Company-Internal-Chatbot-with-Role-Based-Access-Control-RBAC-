from pathlib import Path

def load_markdown_files(base_path="Fintech-data-main"):
    documents = []

    for md_file in Path(base_path).rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "content": text,
            "source": md_file.name,
            "department": md_file.parent.name
        })

    return documents
