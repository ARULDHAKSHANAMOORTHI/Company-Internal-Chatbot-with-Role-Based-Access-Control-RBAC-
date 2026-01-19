from backend.search import search_docs

def test_finance_cannot_access_hr():
    docs = search_docs("employee leave policy", role="finance")
    for d in docs:
        assert "hr" not in d.metadata.get("roles", "")

def test_c_level_access_all():
    docs = search_docs("company policy", role="c_level")
    assert len(docs) > 0
