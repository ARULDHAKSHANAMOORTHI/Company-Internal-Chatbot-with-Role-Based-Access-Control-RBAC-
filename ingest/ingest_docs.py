
# # import os
# # import re
# # import pandas as pd
# # from langchain_core.documents import Document
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.vectorstores import Chroma
# # from langchain_huggingface import HuggingFaceEmbeddings


# # def clean_markdown(text):
# #     lines = text.splitlines()
# #     cleaned = []
# #     last_line = None

# #     for line in lines:
# #         line = line.strip()
# #         if not line:
# #             continue
# #         if line == last_line:
# #             continue
# #         cleaned.append(line)
# #         last_line = line

# #     return "\n".join(cleaned)

# # DATA_DIR = "data/Fintech-data-main"

# # ROLE_MAPPING = {
# #     "finance": "finance,c_level",
# #     "marketing": "marketing,c_level",
# #     "hr": "hr,c_level",
# #     "engineering": "engineering,c_level",
# #     "general": "employees,c_level"
# # }

# # def load_documents():
# #     docs = []

# #     for root, _, files in os.walk(DATA_DIR):
# #         for file in files:
# #             path = os.path.join(root, file)
# #             department = os.path.basename(root).lower()

# #             try:
# #                 if file.endswith(".md"):
# #                     with open(path, encoding="utf-8") as f:
# #                         raw_text = f.read()
# #                         text = clean_markdown(raw_text)

# #                 elif file.endswith(".csv"):
# #                     df = pd.read_csv(path)
# #                     text = df.to_string(index=False)

# #                 else:
# #                     continue

# #                 if not text.strip():
# #                     continue

# #                 docs.append({
# #                     "text": text,
# #                     "source": file,
# #                     "department": department,
# #                     "roles": ROLE_MAPPING.get(department, "employees")
# #                 })

# #             except Exception as e:
# #                 print(f"Skipping {file}: {e}")

# #     return docs


# # def chunk_documents(docs):
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=500,
# #         chunk_overlap=100
# #     )

# #     chunks = []
# #     for doc in docs:
# #         for chunk in splitter.split_text(doc["text"]):
# #             chunks.append({
# #                 "content": chunk,
# #                 "metadata": {
# #                     "source": doc["source"],
# #                     "department": doc["department"],
# #                     "roles": doc["roles"]
# #                 }
# #             })
# #     return chunks

# import os
# import pandas as pd
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# # ==============================
# # CONFIG
# # ==============================
# DATA_DIR = "data/Fintech-data-main"

# ROLE_MAPPING = {
#     "finance": "finance,c_level",
#     "marketing": "marketing,c_level",
#     "hr": "hr,c_level",
#     "engineering": "engineering,c_level",
#     "general": "employees,c_level"
# }


# # ==============================
# # UTILITY FUNCTIONS
# # ==============================
# def clean_markdown(text: str) -> str:
#     """
#     Remove duplicate lines, empty lines, and extra noise from markdown
#     """
#     lines = text.splitlines()
#     cleaned = []
#     last_line = None

#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
#         if line == last_line:
#             continue
#         cleaned.append(line)
#         last_line = line

#     return "\n".join(cleaned)


# # ==============================
# # LOAD DOCUMENTS
# # ==============================
# def load_documents():
#     """
#     Walk through data directory and load markdown & CSV files
#     with role metadata
#     """
#     documents = []

#     for root, _, files in os.walk(DATA_DIR):
#         department = os.path.basename(root).lower()

#         for file in files:
#             path = os.path.join(root, file)

#             try:
#                 # ---------- Markdown ----------
#                 if file.endswith(".md"):
#                     with open(path, encoding="utf-8") as f:
#                         raw_text = f.read()
#                         text = clean_markdown(raw_text)

#                 # ---------- CSV ----------
#                 elif file.endswith(".csv"):
#                     df = pd.read_csv(path)
#                     text = df.to_string(index=False)

#                 else:
#                     continue

#                 if not text.strip():
#                     continue

#                 documents.append(
#                     Document(
#                         page_content=text,
#                         metadata={
#                             "source": file,
#                             "department": department,
#                             "roles": ROLE_MAPPING.get(department, "employees")
#                         }
#                     )
#                 )

#             except Exception as e:
#                 print(f"⚠️ Skipping {file}: {e}")

#     return documents


# # ==============================
# # CHUNK DOCUMENTS
# # ==============================
# def chunk_documents(documents):
#     """
#     Split documents into chunks for vector embedding
#     """
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=100
#     )

#     return splitter.split_documents(documents)


# # ==============================
# # MAIN (OPTIONAL TEST)
# # ==============================
# if __name__ == "__main__":
#     docs = load_documents()
#     chunks = chunk_documents(docs)

#     print(f"✅ Loaded documents: {len(docs)}")
#     print(f"✅ Total chunks created: {len(chunks)}")


import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = "data/Fintech-data-main"

ROLE_MAPPING = {
    "finance": "finance,c_level",
    "marketing": "marketing,c_level",
    "hr": "hr,c_level",
    "engineering": "engineering,c_level",
    "general": "employees,c_level"
}

def clean_text(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(dict.fromkeys(lines))  # remove duplicates


def load_documents():
    documents = []

    for root, _, files in os.walk(DATA_DIR):
        department = os.path.basename(root).lower()

        for file in files:
            path = os.path.join(root, file)

            try:
                if file.endswith(".md"):
                    with open(path, encoding="utf-8") as f:
                        text = clean_text(f.read())

                elif file.endswith(".csv"):
                    df = pd.read_csv(path)
                    text = df.to_string(index=False)

                else:
                    continue

                if not text.strip():
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file,
                            "department": department,
                            "roles": ROLE_MAPPING.get(department, "employees")
                        }
                    )
                )

            except Exception as e:
                print(f"Skipping {file}: {e}")

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)
