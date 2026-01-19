# backend/query_utils.py

import re

def normalize_query(query: str) -> str:
    query = query.lower().strip()
    query = re.sub(r"[^\w\s]", "", query)
    return query
