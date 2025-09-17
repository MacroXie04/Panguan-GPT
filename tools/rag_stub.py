from __future__ import annotations

"""RAG placeholder functions.

This file now contains a basic, self-contained RAG implementation for demonstration.
"""

import numpy as np
from typing import Any, Dict

# Note: The following dependencies need to be installed:
# pip install sentence-transformers faiss-cpu numpy
try:
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError:
    print(
        "Please install required packages: pip install sentence-transformers faiss-cpu numpy"
    )
    faiss = None
    SentenceTransformer = None

# --- Global state for the RAG model (for demonstration) ---

# 1. Load a pre-trained sentence embedding model
# This is done once when the module is loaded.
model = SentenceTransformer("all-MiniLM-L6-v2") if SentenceTransformer else None

# 2. Define a sample document corpus
documents = [
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
    "The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials.",
    "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy.",
    "The pyramids of Giza are ancient masonry structures located on the Giza Plateau in Egypt.",
    "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City.",
    "Artificial intelligence is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.",
    "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn'.",
]

# 3. Embed the documents and create a FAISS index
# This is also done once. In a real application, this index would be pre-built and loaded.
if model and documents:
    document_embeddings = model.encode(documents)
    embedding_dim = document_embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(document_embeddings))
else:
    index = None

# --- End of Global State ---


def retrieve(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Retrieves the top-k most relevant document snippets for a given query.

    This implementation uses a SentenceTransformer model for embeddings and a FAISS
    index for efficient similarity search.

    Args:
        query: The user's query string.
        top_k: The number of documents to retrieve.

    Returns:
        A dictionary containing the status and a list of hits. Each hit is a
        dictionary with a 'score' and the 'document' text.
    """
    if not model or not index:
        return {
            "status": "error",
            "message": "RAG components not initialized. Please install dependencies.",
            "hits": [],
        }

    try:
        # 1. Embed the query
        query_embedding = model.encode([query])

        # 2. Search the index for top-k most similar documents
        distances, indices = index.search(np.array(query_embedding), top_k)

        # 3. Format and return the results
        hits = [
            {"score": float(dist), "document": documents[idx]}
            for dist, idx in zip(distances[0], indices[0])
        ]

        return {"status": "ok", "hits": hits}
    except Exception as e:
        return {"status": "error", "message": str(e), "hits": []}
