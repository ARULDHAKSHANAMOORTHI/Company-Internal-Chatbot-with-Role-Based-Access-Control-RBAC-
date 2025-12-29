from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP
    )
    return splitter.split_text(text)
