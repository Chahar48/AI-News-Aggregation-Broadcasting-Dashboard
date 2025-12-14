# backend/app/services/embedder.py

"""
Embedding service using HuggingFace Sentence Transformers.

Used for:
- Deduplication (semantic similarity)
- Content clustering (optional)
- Improving summaries (future extension)

Model: all-MiniLM-L6-v2
Fast, accurate & industry-standard for semantic similarity tasks.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer, util


class EmbedderService:
    """
    Singleton-style embedding service.
    Loads model once on startup.
    """

    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            print("🔤 Loading embedding model: all-MiniLM-L6-v2 ...")
            cls._model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            print("✅ Embedding model loaded.")
        return cls._model

    # ------------------------------------------------------
    # Generate embeddings for text
    # ------------------------------------------------------
    @classmethod
    def generate_embedding(cls, text: str) -> List[float]:
        if not text:
            return [0.0] * 384  # MiniLM output dim is 384

        model = cls.load_model()
        embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return embedding.tolist()

    # ------------------------------------------------------
    # Compute cosine similarity between two embeddings
    # ------------------------------------------------------
    @staticmethod
    def similarity(vec1: List[float], vec2: List[float]) -> float:
        if not vec1 or not vec2:
            return 0.0

        v1 = np.array(vec1)
        v2 = np.array(vec2)
        sim = float(util.cos_sim(v1, v2)[0][0])
        return sim

    # ------------------------------------------------------
    # Batch embedding helper
    # ------------------------------------------------------
    @classmethod
    def generate_batch_embeddings(cls, texts: List[str]) -> List[List[float]]:
        model = cls.load_model()
        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()


# Create a global shared instance
embedder = EmbedderService()
