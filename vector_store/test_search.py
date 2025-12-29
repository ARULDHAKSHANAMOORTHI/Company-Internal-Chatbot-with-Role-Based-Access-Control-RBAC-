# vector_store/test_search.py

from vector_store.search import semantic_search

queries = [
    ("What is the Q3 revenue?", "Finance"),
    ("Explain employee leave policy", "Marketing"),
    ("Describe system architecture", "Engineering"),
    ("Company financial overview", "Employees"),
    ("Company financial overview", "C-Level")
]

for q, role in queries:
    print(f"\nQuery: {q} | Role: {role}")
    results = semantic_search(q, role)

    for r in results:
        print("-", r["metadata"]["source"])
