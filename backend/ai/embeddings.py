from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
FALLBACK_DIM = 384


@lru_cache(maxsize=1)
def _st_model():
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(MODEL_NAME)
    except Exception:
        return None


@lru_cache(maxsize=1)
def _fallback_vectorizer():
    from sklearn.feature_extraction.text import HashingVectorizer

    return HashingVectorizer(n_features=FALLBACK_DIM, alternate_sign=False, norm=None)


def _normalize(v: np.ndarray) -> np.ndarray:
    denom = float(np.linalg.norm(v))
    if denom == 0.0:
        return v
    return v / denom


def embed_text(text: str) -> List[float]:
    m = _st_model()
    if m is not None:
        v = m.encode([text], normalize_embeddings=True)[0]
        return [float(x) for x in v.tolist()]

    vec = _fallback_vectorizer().transform([text]).toarray().astype(np.float32)[0]
    vec = _normalize(vec)
    return [float(x) for x in vec.tolist()]

