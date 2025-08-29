from __future__ import annotations

"""RAG placeholder functions.

These are stubs to be replaced by a real RAG implementation later.
"""

from typing import Dict


def retrieve(query: str) -> Dict[str, object]:
    """
    Placeholder: return an empty hit list.

    TODO:
    - Connect to a vector store
    - Embed query and retrieve top-k passages
    - Return citations and snippets
    """
    return {"status": "ok", "hits": []}


